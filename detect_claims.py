import spacy
import json
nlp = spacy.load('en')

controversies_sg = [
# regarding tags: [["A"], ["B", "C"]] - contains A and (B or C)
    {'ID' : 0,
     'claim' : 'Ministers do not deserve the salaries they earn.',
     'tags' : [['minister', 'Lee Hsien Loong'], ['million'], ['salaries', 'earn']],
     'quora' : 'https://www.quora.com/Why-are-the-salaries-of-cabinet-ministers-so-high-in-Singapore'
    },
    {'ID' : 1,
     'claim' : 'President Halimah is a puppet.',
     'tags' : [['Halimah'], ['puppet', 'powerless']],
     'quora' : 'https://www.quora.com/Is-the-President-of-Singapore-merely-a-puppet'
    },
    {'ID' : 2,
     'claim' : 'Halimah Yacob changed her race to qualify for presidency.',
     'tags' : [['Halimah'], ['race', 'president'], ['Indian', 'Malay']],
     'quora' : 'https://www.quora.com/Is-it-true-that-Singaporean-MP-Mdm-Halimah-Yacob-is-born-an-Indian-Singaporean-but-is-now-standing-as-a-Malay-presidential-candidate'
    },
    {'ID' : 3,
     'claim' : 'Crony capitalism is a problem in Singapore.',
     'tags' : [['crony'], ['Singapore', 'PAP', 'Lee Hsien Loong']],
     'quora' : 'https://www.quora.com/How-serious-is-Singapores-crony-capitalism-the-tendency-for-entities-related-to-the-ruling-party-to-be-favoured-over-in-the-bidding-for-government-contracts'
    },
    {'ID' : 4,
     'claim' : 'The influx of foreign talent has depressed wages.',
     'tags' : [['foreign talent', 'FT'], ['steal', 'depress']],
     'quora' : 'https://www.quora.com/How-serious-is-Singapores-crony-capitalism-the-tendency-for-entities-related-to-the-ruling-party-to-be-favoured-over-in-the-bidding-for-government-contracts'
    },
    {'ID' : 5,
     'claim' : 'Ho Ching should not be the CEO of Temasek Holdings.',
     'tags' : [['Ho Ching'], ['Temasek'], ['debt', 'lose', 'Lee Hsien Loong']],
     'quora' : 'https://www.quora.com/unanswered/Was-the-appointment-of-Ho-Ching-as-the-CEO-of-Temasek-Holdings-fair-and-has-she-been-effective-at-her-job'
    },
    {'ID' : 6,
     'claim' : 'The government has run out of CPF funds.',
     'tags' : [['CPF'], ['lost']],
     'quora' : 'https://www.quora.com/Where-is-the-evidence-to-the-accusations-that-the-Singapore-government-lost-all-the-money-in-our-CPF-in-overseas-investments'
    },
    {'ID' : 7,
     'claim' : 'The Government has consistently lost money in investments.',
     'tags' : [['GIC', 'MAS', 'CPF'], ['lost']],
     'quora' : 'https://www.quora.com/Where-is-the-evidence-to-the-accusations-that-the-Singapore-government-lost-all-the-money-in-our-CPF-in-overseas-investments'
    },
    {'ID' : 8,
     'claim' : 'CPF interest rates are unfairly low.',
     'tags' : [['CPF'], ['interest'], ['low']],
     'quora' : 'https://www.quora.com/Are-the-interest-rates-of-the-Singapore-CPF-really-unfairly-low'
    },
    {'ID' : 9,
     'claim' : 'The Straits Times is controlled by the government.',
     'tags' : [['state media','government', 'control'], ['Straits Times']],
     'quora' : 'https://www.quora.com/unanswered/How-much-control-does-the-government-have-over-The-Straits-Times'
    }
]


    
# print(controversies_sg_)

def detect_claims(article_text):
    
    controversies_sg_ = []
    for claim in controversies_sg:
        tags_lemma = []
        for tag in claim['tags']:

            tag_lemma = []
            for item in tag:
                tag_lemma.append(" ".join([token.lemma_ for token in nlp(item)]))
            tags_lemma.append(tag_lemma)

        claim['tags_lemma'] = tags_lemma
        controversies_sg_.append(claim)
    
    '''
    input: article_text
    
    output: list of claims detected
    {detected: [
        {'claim' : 'Ministers do not deserve the salaries they earn.',
         'quora' : 'https://www.quora.com/Why-are-the-salaries-of-cabinet-ministers-so-high-in-Singapore',
         'sentence' : 'Millionaire minister Khaw Boon Wan ...'
        },
        {'claim' : 'Ministers do not deserve the salaries they earn.',
         'quora' : 'https://www.quora.com/Is-the-President-of-Singapore-merely-a-puppet',
         'sentence' : 'Puppet President Halimah once again ...'
        },
    ]}
    '''
    
    document = nlp(article_text)
    sent_text = list(document.sents)

    detected = []

    for sentence in sent_text:
        doc = sentence
        sent_lemmas = " ".join([token.lemma_ for token in doc])

        for claim in controversies_sg_:

            contains_all_tags = True

            for tag in claim["tags_lemma"]:

                contains_item = False
                for item in tag:
                    if item in sent_lemmas:
                        contains_item = True
                if not contains_item:
                    contains_all_tags = False

            if contains_all_tags:
                claim_detected = {}
                claim_detected["claim"] = claim["claim"]
                claim_detected["quora"] = claim["quora"]
                claim_detected["sentence"] = str(sentence)
                detected.append(claim_detected)
                print(claim["claim"])
                print(sentence)
                print()
                
    print({"detected" : detected})
    return json.dumps({"detected" : detected})