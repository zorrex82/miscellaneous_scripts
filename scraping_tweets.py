from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import csv

now = datetime.now()
now = now.strftime('%Y-%m-%d')
yesterday = datetime.now() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')


def main():
    keyword = input('Informe um usuário ou tópico para buscar: ')
    maxTweets = int(input("Selecione a quantidade de tweets para buscar: "))

    # Iniciando um arquivo csv vazio para manipular
    csvFile = open(keyword + '-sentiment-' + now + '.csv', 'a', newline='', encoding='utf8')

    # Usando csv writer para abrir o arquivo para escrita e definir suas colunas
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['id', 'date', 'tweet', ])

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            keyword + ' since:' + yesterday + ' until:' + now + ' -filter:links -filter:replies').get_items()):
        if i > maxTweets:
            break
        csvWriter.writerow([tweet.id, tweet.date, tweet.content])
    csvFile.close()

    # iniciando a analise de sentimentos
    analyzer = SentimentIntensityAnalyzer()

    # Lendo o CSV de volta em nosso programa
    df = pd.read_csv('~/Documents/PycharmProjects/Diversos/webscrap/' + keyword + '-sentiment-' + now + '.csv',
                     parse_dates=True, index_col=0)

    # Criando as colunas de sentimentos
    df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df['tweet']]
    df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet']]
    df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet']]
    df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet']]

    # Pegando a media dos sentimentos de cada coluna
    avg_compound = np.average(df['compound'])
    avg_neg = np.average(df['neg']) * -1
    avg_neu = np.average(df['neu'])
    avg_pos = np.average(df['pos'])

    # Contagem dos tweets
    count = len(df.index)

    # Print das analises
    print("Foram encontrados ", count, "tweets sobre " + keyword, end='\n*')
    print("Sentimentos positivos:", '%.2f' % avg_pos, end='\n*')
    print("Sentimentos neutros:", '%.2f' % avg_neu, end='\n*')
    print("Sentimentos negativos:", '%.2f' % avg_neg, end='\n*')
    print("Sentimentos compostos:", '%.2f' % avg_compound, end='\n')


if __name__ == '__main__':
    main()
