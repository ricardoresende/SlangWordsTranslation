import psycopg2
import unidecode
import csv
import os

try:
   connection = psycopg2.connect(user="xxxxx", password="xxxx", host="999.999.999.99", port="5432", database="rrm")
   cursor = connection.cursor()
   os.system('cls')
   print("\n","##### PostgreSQL connection is open #####", "\n")

   postgreSQL_select_Query = "SELECT p.idpostagem, p.mensagemoriginal, cc.nomeoriginal FROM  postagem p INNER JOIN classificacaocubo cc USING(idclassificacao) WHERE p.postcandidata IN ('TALVEZ','SIM') AND idclassificacao IS NOT NULL;"
   cursor.execute(postgreSQL_select_Query)
   posts_records = cursor.fetchall() 

   qtdePosts = cursor.rowcount

   postgreSQL_select_Query = "SELECT e.descricao, e.dssignificado, e.quantpalavras FROM expressaocategorizada e ORDER BY e.quantpalavras DESC;"
   cursor.execute(postgreSQL_select_Query)
   expression_records = cursor.fetchall() 
   
   qtdeExpressions = cursor.rowcount
   
   arrayPosts = []

   for i in range(0, qtdePosts):
       sentence = unidecode.unidecode(posts_records[i][1].lower())
       sentence = sentence.replace(";","")
       arrayPosts.append([posts_records[i][0], sentence, unidecode.unidecode(posts_records[i][2].lower()), sentence])

   arrayExpressions = []

   for i in range(0, qtdeExpressions):
       arrayExpressions.append([unidecode.unidecode(expression_records[i][0].lower()), unidecode.unidecode(expression_records[i][1].lower()), expression_records[i][2]])

   for x in range(0, qtdePosts):
     for y in range(0, qtdeExpressions):
       if arrayExpressions[y][2] > 1:
         arrayPosts[x][1] = arrayPosts[x][1].replace(arrayExpressions[y][0], arrayExpressions[y][1])
       else:
         arraySentence = arrayPosts[x][1].split()
         newSentence = ""
         for z in arraySentence:
           
           if z == unidecode.unidecode(arrayExpressions[y][0].lower()):
             z = unidecode.unidecode(arrayExpressions[y][1].lower())
           
           newSentence = newSentence + " " + z           

         arrayPosts[x][1] = newSentence[1:]

   import csv
   with open('newExpressions.csv', 'w', newline='') as file:
       writer = csv.writer(file, delimiter=';')
       #for x in arrayPosts : writer.writerow ([x[0],x[3],x[1],x[2]])
       for x in arrayPosts : writer.writerow ([x[1],x[2]])

     #print(arrayPosts[x][1])
     #print(arrayPosts[x][3],"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("\n","##### PostgreSQL connection is closed #####")