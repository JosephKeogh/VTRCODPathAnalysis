rm combined.txt

cat trips0.csv >> combined.txt
echo >> combined.txt

cat trips1.csv >> combined.txt
echo >> combined.txt

cat trips2.csv >> combined.txt
echo >> combined.txt

cat trips3.csv >> combined.txt
echo >> combined.txt

cat trips4.csv >> combined.txt
echo >> combined.txt

split -d 3 -50000 --additional-suffix=.csv combined.txt smaller-

rm combined.txt