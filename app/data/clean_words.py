from collections import defaultdict
skip_stats = defaultdict(int)
with open('dict.txt.zhtw.sort') as f:
    data = f.readlines()
    with open('dict.txt.zhtw.trimsize', 'w') as f_out:
        for row in data:
            word = row.split(' ')[0]
            if len(word) == 1:
                skip_stats[len(word)] += 1
                print(f'skip {word}')
                continue
            elif len(word) > 5:
                skip_stats[len(word)] += 1
                print(f'skip {word}')
                continue
            else:
                f_out.write(row)
print(skip_stats)
