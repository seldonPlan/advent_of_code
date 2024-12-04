# ripgrep to find leftmost and rightmost digits

rg '^([a-z]+)?(?P<num>[0-9]).*$' -r '$num' -N ./input.txt > output_left.txt
rg '^.*(?P<num>[0-9])([a-z]+)?$' -r '$num' -N ./input.txt > output_right.txt

# combine the left and right results into a single number
paste -d '' output_left.txt output_right.txt > output.txt

# sum the output numbers for the whole file
awk '{ sum += $1 } END { print sum }' output.txt


# or combine everything into one line
awk '{ sum += $1 } END { print sum }' <(paste -d '' <(rg '^([a-z]+)?(?P<num>[0-9]).*$' -r '$num' -N input.txt) <(rg '^.*(?P<num>[0-9])([a-z]+)?$' -r '$num' -N input.txt))