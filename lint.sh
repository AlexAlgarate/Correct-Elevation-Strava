directories=("src" "tests")
for dir in "${directories[@]}"; do
    isort $dir && black $dir && ruff check $dir
done