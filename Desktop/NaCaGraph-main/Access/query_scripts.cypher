//Example 1: Query the distribution of triggers, articles and topics with event_type is ”catastrophe” after 2020.
MATCH p=(:Topic )-[r1:PUBLISHED_TIME]->(arti:Article)-[r2:HAS_TRIGGER {text:"type:catastrophe"} ]->(n:IdTrigger) where toInteger(right(r1.text,4)) >2020 
return p;

//Example 2.1:Visual map of all relevant event_types, role_labels and arguments of trigger ”fire”.
match (:IdTrigger{text:"fire"})-->(idarg:IdArgument)
match p=(:EventType)-->(:Trigger{text:"fire"})-->(:RoleLabel)-->(:Argument{text:idarg.text})
return p;

//Example 2.2: Visual map of the distribution topic, article and argument and published year of trigger ”fire”.
match  p=(t:Topic)-->(arti:Article)-[et:HAS_TRIGGER]->(idtr:IdTrigger{text:"fire"})-[rl:HAS_ARGUMENT]->(:IdArgument )  
match (y:Year)-->(arti)
return p,y;

//Example 2.3: Count the frequency of trigger ”fire” under each topic in different year after 2003.
match p=(topic:Topic)-[r1:PUBLISHED_TIME]->(arti:Article)-->(idtr:IdTrigger{text:"fire"})
match (topic)-[r1]->(arti)-->(:EventType)-->(tr:Trigger{text:idtr.text})
match (year:Year)-->(arti)
where toInteger(right(r1.text,4))>2003
with topic,year,count(tr) as num_tr
return topic.text as Topic, toInteger(year.text) as Year, num_tr as num_trigger
order by Topic,Year desc;

//Example 3.1: Count the first ten triggers per topic, return topics, ten triggers, ten frequency numbers.
match p=(topic:Topic)-[r1:PUBLISHED_TIME]->(arti:Article)-->(idtr:IdTrigger)
match (topic)-[r1]->(arti)-->(:EventType)-->(tr:Trigger{text:idtr.text})
match (year:Year)-->(arti)
with topic,tr,count(tr) as num_tr
order by num_tr desc
WITH topic, collect(tr.text)[0..10] AS triggers, collect(num_tr)[0..10] AS num_triggers
RETURN topic.text as topic, triggers,num_triggers;

//Example 3.2: Count the first ten event types per topic, return topics, ten event_tpyes/triggers, ten frequency numbers.
match p=(topic:Topic)-[r1:PUBLISHED_TIME]->(arti:Article)-->(et:EventType)
with topic,et,count(et) as num_et
order by num_et desc
WITH topic, collect(et.text)[0..10] AS event_types, collect( num_et )[0..10] AS num_event_types
RETURN topic.text as topic, event_types, num_event_types;

//Graph visualization for schema
CALL db.schema.visualization();

//Download Graph style
:style;
