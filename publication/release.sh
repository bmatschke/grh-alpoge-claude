#!/usr/bin/env bash
# Publish the output already built for EDITION_TAG at RELEASE_REVISION.
set -euo pipefail
tag="${EDITION_TAG:?}"
revision="${RELEASE_REVISION:?}"
directory="${1:?pass the build output directory}"
[[ $tag =~ ^edition-[0-9]+(\.[0-9]+)*$ ]]
[[ $revision =~ ^[0-9a-f]{40}$ ]]
assets=(overview.pdf full.pdf proof-source.zip)
for asset in "${assets[@]}"; do test -s "$directory/$asset"; done

existing_tag=$(git rev-parse -q --verify "refs/tags/$tag^{commit}" || true)
if [[ -n "$existing_tag" && "$existing_tag" != "$revision" ]]; then
  echo "Tag $tag already identifies $existing_tag, expected $revision." >&2
  exit 1
fi

scratch=$(mktemp -d)
metadata="$scratch/metadata.json"
trap 'rm -rf "$scratch"' EXIT
if gh release view "$tag" --json isDraft,targetCommitish,assets > "$metadata"; then
  if [[ $(jq -r '.isDraft' "$metadata") == false ]]; then
    test "$existing_tag" = "$revision"
    for asset in "${assets[@]}"; do
      jq -e --arg name "$asset" '.assets | any(.name == $name and .size > 0)' "$metadata" > /dev/null
    done
    echo "$tag has been published at this commit with all three assets."
    exit 0
  fi
  if [[ -z "$existing_tag" && $(jq -r .targetCommitish "$metadata") != "$revision" ]]; then
    echo "The existing draft names a different target. Check the draft before publishing." >&2
    exit 1
  fi
else
  notes="publication/editions/$tag.md"
  if [[ -f "$notes" ]]; then
    note_args=(--notes-file "$notes")
  else
    note_args=(--notes "Overview, detailed edition, and typesetting sources for commit $revision.")
  fi
  gh release create "$tag" --draft --target "$revision" --title "Manuscript $tag" "${note_args[@]}"
fi
# An interrupted draft may contain earlier uploads. Verify those and add only missing files.
gh release view "$tag" --json assets > "$metadata"
for asset in "${assets[@]}"; do
  if jq -e --arg name "$asset" '.assets | any(.name == $name)' "$metadata" > /dev/null; then
    gh release download "$tag" --pattern "$asset" --dir "$scratch"
    cmp "$scratch/$asset" "$directory/$asset"
  else
    gh release upload "$tag" "$directory/$asset"
  fi
done
current=$(git show origin/main:publication/edition.txt 2>/dev/null || cat publication/edition.txt)
latest=false
if [[ "$tag" == "$current" ]]; then latest=true; fi
gh release edit "$tag" --draft=false "--latest=$latest"
