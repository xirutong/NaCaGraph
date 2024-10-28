from py2neo import Graph
import os

"""
    Connection: In the terminal, go to the "\neo4j-community-4.4.21\bin" directory 
                and execute the command "neo4j console" first to link the web neo4j database.
    Running this program will automatically run the word cypher command to create a Graph in the neo4j database.
"""

#Log in to the database.
passport='neo4jneo4j'
graph_the = Graph("bolt://localhost:7687", auth=('neo4j', passport), name='neo4j')

def create_graph(xml_path, topics):
    global graph_the
    for i in topics:
        create_command = '''CALL apoc.load.xml("file:''' + xml_path + i + '''.xml")
        YIELD value
        WITH value, value.topic AS topic_text
        MERGE (t: Topic {text: topic_text, type:"topic"} )

        WITH value, t
        UNWIND value._children AS article
        WITH t, article.aid AS articleId, article.url as articleURL,
            [item in article._children WHERE item._type = "title"][0] AS title,
            [item in article._children WHERE item._type = "date"][0] AS date,
            [item in article._children WHERE item._type = "event"] AS events
        MERGE ( a:Article {text:title._text, type:"article", aurl:articleURL})
        MERGE ( dat:Year {text: right(date._text,4), type:'year'})
        
        MERGE (t)-[:PUBLISHED_TIME {text: date._text}]->(a)
        MERGE (dat)-[:PUBLISHED_ARTICLE ]->(a)

        WITH events, a,articleId,articleURL
        UNWIND events AS event
        WITH a,articleId,articleURL,
            [item in event._children WHERE item._type = "trigger"][0] AS trigger,
            [item in event._children WHERE item._type = "type"][0] AS event_type,
            [item in event._children WHERE item._type = "argument"] AS arguments

        WHERE NOT trigger._text IS NULL
        MERGE (et:EventType {text:"type:"+event_type._text, type:'event_type'})
        MERGE (tr: Trigger {text: trigger._text, type:"trigger"})
        MERGE (idtr: IdTrigger {text: trigger._text, type:"idtrigger", aid:articleId, aurl:articleURL, eventType:event_type._text } )
    
        MERGE (et)-[:EVENT_FOR]->(tr)
        MERGE (et)-[:EVENT_FOR_IDTR]->(idtr)
        MERGE (a)-[:HAS_EVENT_TYPE { aid:articleId, aurl:articleURL }]->(et)
        MERGE (a)-[:HAS_TRIGGER {text:"type:"+event_type._text, aid:articleId, aurl:articleURL}]->(idtr)

        WITH arguments, tr,idtr,articleId,articleURL, event_type._text as et_text, trigger._text as tr_text
        UNWIND arguments AS argument
        WITH tr,idtr,articleId,articleURL, et_text,tr_text, 
            [item in argument._children WHERE item._type = "mention"][0] AS argument,
            [item in argument._children WHERE item._type = "role"][0] AS argument_role

        WHERE NOT argument._text IS NULL
        MERGE (ro:RoleLabel {text: "role:"+argument_role._text, type:"role_label"})
        MERGE (arg:Argument {text: argument._text, type:"argument"})
        MERGE (idarg: IdArgument {text: argument._text, type:"idargument", aid:articleId, aurl:articleURL,eventType:et_text, trigger:tr_text,roleLabel:argument_role._text })
        
        MERGE (tr)-[: TR_OF ]->(ro)
        MERGE (ro)-[: ROLE_FOR]->(arg)
        MERGE (ro)-[: ROLE_FOR_IDARG]->(idarg)
        MERGE (idtr)-[:HAS_ROLE {aid:articleId, aurl:articleURL} ]->(ro)
        MERGE (idtr)-[: HAS_ARGUMENT {text: "role:"+argument_role._text, aid:articleId, aurl:articleURL} ]->(idarg)
        '''
        graph_the.run(create_command)

#xml files are in "/Prepare/events2xml_results/"
xml_path = os.path.dirname(
    os.path.abspath(os.path.dirname(os.getcwd())) + '/Prepare/events2xml_results/'  # The previous directory of the printed file
)
xml_path = xml_path.replace('\\', '/')
xml_path=xml_path+"/"
print(xml_path)
topics = ['drought', 'climate_change', 'earthquake', 'forest_fire', 'greenhouse', 'high_temperature', 'wildfire']
create_graph(xml_path, topics)



