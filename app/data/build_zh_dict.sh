# install homebrew (skip if already installed)
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null

# install opencc
brew install opencc

# https://github.com/BYVoid/OpenCC
# s2tw.json Simplified Chinese to Traditional Chinese (Taiwan Standard) 簡體到臺灣正體
# s2twp.json Simplified Chinese to Traditional Chinese (Taiwan Standard) with Taiwanese idiom 簡體到繁體（臺灣正體標準）並轉換爲臺灣常用詞彙(e.g. 網絡->網路, 鼠標->滑鼠等)
opencc -i dict.txt.big -o dict.txt.zhtw -c s2twp.json

# sort to dedup dictionary file
sort dict.txt.zhtw | uniq | sort  > dict.txt.zhtw.sort

# 移除一個字的詞與超過五個字的詞
python clean_words.py
