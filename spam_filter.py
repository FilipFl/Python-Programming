import os
import sys
import glob
import re
import xml.dom.minidom

# task given was to label mails in a given directory and create a spam probability filter using naive Bayesian method
# and laplacian smoothing

# W programie znajdują się osobne słowniki dla prawdopobieństwa Bayesa i Laplace'a, na koniec słownik z xml
# został połączony ze słownikiem dla prawdopodobieństwa Bayesa

hamdict = {}
spamdict = {}
probability_spamdict = {}
probability_hamdict = {}
laplace_prob_spamdict = {}
laplace_prob_hamdict = {}
all_words = []
k = 2
types = 2

def mail_into_dict(mail):
    words = mail.get_words()
    cat = mail.get_cat()
    if (cat=="spam"):
        for element in words:
            if element not in all_words:
                all_words.append(element)
            if element in spamdict:
                spamdict[element] += 1
            else:
                spamdict[element] = 1
    elif (cat =="ham"):
        for element in words:
            if element not in all_words:
                all_words.append(element)
            if element in hamdict:
                hamdict[element] += 1
            else:
                hamdict[element] = 1


class Mail:
    def __init__(self):
        self.category = ""
        self.sender = ""
        self.receiver = ""
        self.date = ""
        self.subject = ""
        self.content = ""

    def get_email(self, file_name):
        new_mail = open("spam/" + file_name, "r")
        mail_category = file_name.split()
        self.category = mail_category[0]
        parts = []
        for line in new_mail:
            line = line.replace('\t', '')
            line = line.replace('\n', '')
            separate = line.split(":")
            for i in range(len(separate)):
                separate[i] = separate[i].lstrip()
                separate[i] = separate[i].rstrip()
            parts.append(separate)
        self.sender = parts[0][1]
        self.receiver = parts[1][1]
        self.date = parts[2][1] +":" +parts[2][2]
        self.subject = parts[3][1]
        self.content = parts[4][1]

    def show_email(self):
        print("Nadawca: " + self.sender)
        print("Odbiorca: " + self.receiver)
        print("Data: " + self.date)
        print("Tytuł: " + self.subject)
        print("Treść: " + self.content)

    def get_cat(self):
        return self.category

    def get_words(self):
        words = self.content.split()
        for j in range(len(words)):
            for i in range(len(words[j])):
                if not words[j][i].isalpha():
                    words[j] = words[j].replace(words[j][i],'')
            words[j] = words[j].lower()
        return words

    def get_good_probability(self, prob1, prob2):
        list_of_words = self.get_words()
        prob_for_spam_words = 1.0
        prob_for_ham_words = 1.0
        for word in list_of_words:
            if word in probability_spamdict:
                prob_for_spam_words = prob_for_spam_words * probability_spamdict[word]
            if word in probability_hamdict:
                prob_for_ham_words = prob_for_ham_words * probability_hamdict[word]
        return (prob_for_spam_words * prob1) / ((prob_for_spam_words * prob1) + (prob_for_ham_words * prob2))

    def get_good_laplace_probability(self, prob1, prob2, countsp, counth):
        list_of_words = self.get_words()
        prob_for_spam_words = 1
        prob_for_ham_words = 1
        for word in list_of_words:
            if word in laplace_prob_spamdict:
                prob_for_spam_words = prob_for_spam_words * (laplace_prob_spamdict[word])
            else:
                prob_for_spam_words = prob_for_spam_words * (k/(countsp+(k*types)))
            if word in laplace_prob_hamdict:
                prob_for_ham_words = prob_for_ham_words * laplace_prob_hamdict[word]
            else:
                prob_for_ham_words = prob_for_ham_words * (k / (counth + (k * types)))
        return (prob_for_spam_words * prob1) / (
                (prob_for_spam_words * prob1) + (prob_for_ham_words * prob2))


mails_dir = "./spam"
file_names = glob.glob(str(mails_dir) + '\\*.txt')
mails = []
for file in file_names:
    name = file.split('\\')[-1]
    m = Mail()
    m.get_email(name)
    mails.append(m)

spam_count = 0
ham_count = 0
messages_count = 0

for mail in mails:
    mail_into_dict(mail)
    if mail.get_cat() == "spam":
        spam_count += 1
        messages_count += 1
    elif mail.get_cat() == "ham":
        ham_count +=1
        messages_count +=1

count_in_spam = 0
count_in_ham = 0

for x in spamdict:
    count_in_spam += spamdict[x]
for x in hamdict:
    count_in_ham += hamdict[x]

for x in spamdict:
    probability_spamdict[x] = (spamdict[x]/count_in_spam)
for x in hamdict:
    probability_hamdict[x] = (hamdict[x]/count_in_ham)
for x in spamdict:
    laplace_prob_spamdict[x] = ((spamdict[x]+k)/(count_in_spam+(k*types)))
for x in hamdict:
    laplace_prob_hamdict[x] = ((hamdict[x]+k)/(count_in_ham+(k*types)))


spam_prob = spam_count/messages_count
ham_prob = ham_count/messages_count
laplace_spam = (spam_count+k)/(messages_count+(k*types))
laplace_ham = (ham_count+k)/(messages_count+(k*types))
index = 0
mails[index].show_email()
prob = mails[index].get_good_probability(spam_prob,ham_prob)
laplace_prob = mails[index].get_good_laplace_probability(laplace_spam,laplace_ham,count_in_spam,count_in_ham)
print("Metodą standardową \"naiwną\" Bayesa prawdopodobieństwo spamu wynosi: " + str(prob))
print("Metodą z wykorzystaniem wygładzenia Laplace'a prawdopodobieństwo spamu wynosi: " + str(laplace_prob))


doc = xml.dom.minidom.parse("spam/dict.xml")
xml_words = doc.getElementsByTagName("word")
for x in xml_words:
    curr_cat = x.getAttribute("type")
    curr_prob = x.getAttribute("probabilty")
    curr_word = x.childNodes[0].nodeValue
    if curr_word not in probability_spamdict:
        if(curr_cat=="spam"):
            probability_spamdict[curr_word] = curr_prob
    if curr_word not in probability_hamdict:
        if(curr_cat=="ham"):
            probability_hamdict[curr_word] = curr_prob



