import fugashi


if __name__ == '__main__':
    # This is our sample text.
    # "Fugashi" is a Japanese snack primarily made of gluten.
    text = "麩菓子は、麩を主材料とした日本の菓子。"

    # The Tagger object holds state about the dictionary.
    tagger = fugashi.Tagger()

    words = [word.surface for word in tagger(text)]
    print(*words)
    # => 麩 菓子 は 、 麩 を 主材 料 と し た 日本 の 菓子 。

    words = tagger(text)
    for word in words:
        print(word)
