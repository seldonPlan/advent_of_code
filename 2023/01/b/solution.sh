
# input needs amended with replacements of actual numbers
# several overlapping results like oneight and sevenine exist, and all need accounted for
sed -e 's/one/o1e/g' -e 's/two/t2o/g' -e 's/three/t3e/g' -e 's/four/f4r/g' -e 's/five/f5e/g' -e 's/six/s6x/g' -e 's/seven/s7n/g' -e 's/eight/e8t/g' -e 's/nine/n9e/g' input.txt

# proceed like part a, but replace all input.txt with <({sed invocation})

# ripgrep to find leftmost and rightmost digits
rg '^([a-z]+)?(?P<num>[0-9]).*$' -r '$num' -N <(sed -e 's/one/o1e/g' -e 's/two/t2o/g' -e 's/three/t3e/g' -e 's/four/f4r/g' -e 's/five/f5e/g' -e 's/six/s6x/g' -e 's/seven/s7n/g' -e 's/eight/e8t/g' -e 's/nine/n9e/g' input.txt) > output_left.txt
rg '^.*(?P<num>[0-9])([a-z]+)?$' -r '$num' -N <(sed -e 's/one/o1e/g' -e 's/two/t2o/g' -e 's/three/t3e/g' -e 's/four/f4r/g' -e 's/five/f5e/g' -e 's/six/s6x/g' -e 's/seven/s7n/g' -e 's/eight/e8t/g' -e 's/nine/n9e/g' input.txt) > output_right.txt

# combine the left and right results into a single number
paste -d '' output_left.txt output_right.txt > output.txt

# sum the output numbers for the whole file
awk '{ sum += $1 } END { print sum }' output.txt


# or combine everything into one invocation
awk '{ sum += $1 } END { print sum }' <(paste -d '' \
    <(rg '^([a-z]+)?(?P<num>[0-9]).*$' -r '$num' -N <(sed -e 's/one/o1e/g' -e 's/two/t2o/g' -e 's/three/t3e/g' -e 's/four/f4r/g' -e 's/five/f5e/g' -e 's/six/s6x/g' -e 's/seven/s7n/g' -e 's/eight/e8t/g' -e 's/nine/n9e/g' input.txt)) \
    <(rg '^.*(?P<num>[0-9])([a-z]+)?$' -r '$num' -N <(sed -e 's/one/o1e/g' -e 's/two/t2o/g' -e 's/three/t3e/g' -e 's/four/f4r/g' -e 's/five/f5e/g' -e 's/six/s6x/g' -e 's/seven/s7n/g' -e 's/eight/e8t/g' -e 's/nine/n9e/g' input.txt)) \
)
