files=()

for f in ebay_data/items-*.json; do
  files+=("$f")
done

python skeleton_parser.py "${files[@]}"
