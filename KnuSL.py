import json

class KnuSL():
    def data_list(wordname):
        with open('/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
                data = json.load(f)
        result = ['None','None']
        for i in range(0, len(data)):
            if data[i]['word'] == wordname:
                result.pop()
                result.pop()
                result.append(data[i]['word_root'])
                result.append(data[i]['polarity'])	

        r_word = result[0]
        s_word = result[1]

        print('어근 : ' + r_word)
        print('극성 : ' + s_word)


        return r_word, s_word
