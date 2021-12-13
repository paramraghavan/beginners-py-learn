'''
Create background image for online work meetings and interviews.
Referenced from :
https://towardsdatascience.com/fun-valentines-day-gift-ideas-for-python-programmers-a27e87b9211b
'''
from wordcloud import WordCloud, STOPWORDS
import imageio
import matplotlib.pyplot as plt

text = 'bigdata,pyspark,aws,s3,emr,lambda,'\
    'api_gateway,dynamodb,elb,glue,iam,code_commit,redshift,docker, aws_batch,'\
    'ci_cd,serverless_framework,rds,java,python,shell_scripting,sql,neo4j,pyflask' \
       ',aurora, oracle, postgres'


print(STOPWORDS)
wordcloud = WordCloud(width=1900,
                      height=1080,
                      prefer_horizontal=0.5,
                      #background_color="rgba(255, 255, 255, 0)",
                      #mode="RGBA"
                      ).generate(text)

#plt.imshow(wordcloud, interpolation='bilinear')
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
wordcloud.to_file("zoom_background.png")
#plt.savefig("simple.png")
#wordcloud.to_file("simple.png")