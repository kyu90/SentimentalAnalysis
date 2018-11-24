import KnuSL
import Scraping

ksl = KnuSL

print("\nKNU 한국어 감성사전입니다~ :)")
print("사전에 단어가 없는 경우 결과가 None으로 나타납니다!!!")
print("-2:매우 부정, -1:부정, 0:중립 or Unkwon, 1:긍정, 2:매우 긍정")
print("\n")	

wordname = df['description']
result = []
wordname = wordname.apply(lambda x: x.split(' '))
for i in range(0, len(wordname)):
    temp = wordname.iloc[i]
    temp2 = 0
    for j in range(0, len(temp)):
        r_word, s_word = ksl.data_list(temp[j])
        try:
            temp2 = temp2+int(s_word)
        except:
            pass
    result.append(temp2)
