# Expects that the environment variables BASE_URL and REMOVE_BG_API_KEY have
# been set.

if [ -z "$1" ]; then
    echo "usage: batch.sh <folder>" >&2
    exit 1
fi

# Loop through all the subfolders of a given folder.
for f in $1/*; do
    if [ -d "$f" ]; then
        printf "$f\n\n"
        python3 livros_35.py rename-images $f
        python3 livros_35.py apply-images-orientation $f
        python3 livros_35.py make-cover $f
        python3 livros_35.py print-image-urls --base-url $BASE_URL $f
    fi
    printf "\n"
done
