CSV_FILE=~/Dropbox/bin/data/lovihatibot.csv

DEDUPE=/tmp/lovihatibot.csv
rm $DEDUPE
awk '!a[$0]++' $CSV_FILE > $DEDUPE

# Remove douchebag spambot
grep -v ",@.* I love the word douchebag. http://t.co/" $DEDUPE > /tmp/tmp.csv
mv /tmp/tmp.csv $DEDUPE

rm /tmp/*ed_words.tmp
grep -i ",I love the word," $DEDUPE > /tmp/loved_words.tmp
grep -i ",I hate the word," $DEDUPE > /tmp/hated_words.tmp

# Slice out first column containing just the loved/hated word
rm /tmp/*ed_words.lst
cat /tmp/loved_words.tmp | cut -d, -f1 > /tmp/loved_words.lst
cat /tmp/hated_words.tmp | cut -d, -f1 > /tmp/hated_words.lst
# cat $DEDUPE              | cut -d, -f1 > /tmp/loved_and_hated_words.lst

# Find top 20s
for f in loved hated # loved_and_hated
do
    most_frequent_words.py -n 20 "/tmp/${f}_words.lst"
done

# Make word clouds (uses https://github.com/hugovk/word_cloud)

rm /tmp/*ed_words.png
for f in loved hated # loved_and_hated
do
    echo "Create word cloud of $f words"
    python ~/Dropbox/bin/word_cloud/wordcloud.py --stopwords None --width 1024 --height 576 --fontfile "/Library/Fonts/Times New Roman.ttf" "/tmp/${f}_words.lst" -o "/tmp/${f}_words.png"
done

echo "Done."
