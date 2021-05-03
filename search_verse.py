import bible_ui as bi
import convert as cvt
import numpy as np


# ASV is the english bible txt
def search_verse(verse_arr,ASV,key):
    if key != "None":

        # Bold the text
        print('\033[1m' + "\n\n對於關鍵詞：%s，結果是:"%(key))
        print ('\033[0m')

        # Set the verse to be an array
        # The print out verses is from the bi.search.
        verse_arr1 = str(bi.search(verse_arr,ASV,str(key)))

        # for reading the data, there are anonying strings
        annoy_str = r"', '"
        verse_arr1 = verse_arr1.replace(annoy_str,"\n")
        verse_arr1 = verse_arr1.split("\n")
        return verse_arr1

    # if there is no arguement input return the original array
    else:
        return verse_arr



# This function is built to seperate the book, chapter and verse
def sep_chapter(location):
    for i in range(len(location)):
        if (location[i].isdigit()):
            global book; global verse
            book = location[:i]
            verse = location[i:]
            break
    return book, verse


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='请输入圣经查找關鍵字,默认繁体字')
    parser.add_argument("key1",
                        type=str,
                        default = "None",
                        nargs='?',
                        help="搜索经文格式：關鍵詞1 2 3 4 簡or繁）\
                        \n 默認繁體字")
    parser.add_argument("key2",
                        type=str,
                        default = "None",
                        nargs='?',
                        help="第二關鍵詞")
    parser.add_argument("key3",
                        type=str,
                        default = "None",
                        nargs='?',
                        help="第三關鍵詞")

    parser.add_argument("key4",
                        type=str,
                        default = "None",
                        nargs='?',
                        help="第四關鍵詞")

    parser.add_argument("version",
                        type=str,
                        default = "T",
                        nargs = '?',
                        help="简体(S) or 繁体(T) ")

    parser.add_argument("English",
                        type=str,
                        default = "N",
                        nargs = '?',
                        help="顯示英文(Y) or 不顯示英文(N) ")


    # Read in the arguements
    args = parser.parse_args()

    # determine if English is used
    ASV = bi.read_text_EN(args.English)
    # Determine which chinese version is used
    CHN = bi.read_text_ZH(args.version)


    # if no argument input, then return an array
    if args.key1 == "None":
        raise ValueError("\n請輸入關鍵詞！")

    else:
        #print(args.version) # Which version are you using
        verses = search_verse(CHN,ASV,args.key1)
        verses = search_verse(verses,ASV,args.key2)
        verses = search_verse(verses,ASV,args.key3)
        verses = search_verse(verses,ASV,args.key4)


    # Final output verse for paste (Not the print out)
    final_verses = ""
    for i in verses:
        # Add space bewteen each spaces
        final_verses += i + "\n\n"

    # If you want to copy the verses or not
    copy = str(input("\nCopy? 「是 or 否（Just hit Enter）」: "))
    if copy == "是":
        #print(verses)
        bi.copy_paste(final_verses)
