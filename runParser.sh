files=()

for f in ebay_data/items-*.json; do
  files+=("$f")
done

python skeleton_parser.py "${files[@]}"


sqlite3 AuctionBase<create.sql
sqlite3 AuctionBase<load.txt