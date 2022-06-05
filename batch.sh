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
        python3 livros_35.py $f rename-images
        python3 livros_35.py $f apply-images-orientation
        python3 livros_35.py $f make-cover
        python3 livros_35.py $f print-image-urls --base-url $BASE_URL
    fi
    printf "\n"
done
