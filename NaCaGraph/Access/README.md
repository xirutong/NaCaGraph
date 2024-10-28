# The Access part of the project.

This directory contains the following contents:

- Query_Example_Results: The directory containing query example results files and codes for processing results.
	- example1.svg, example2.1.svg and example2.2.svg: graph results of example 1, example 2.1 and example 2.2;
	- example2.3_fire.json: json result of example 2.3;
	- example3_eventtype.json and example3_trigger.json: json result of example 3;
	- draw_example2.3_fire.py: code to process example 2.3 result;
	- draw_example3_similarity.py: code to process example 3 result.

- Create_Graph.py: 
	Running this Python file will automatically execute the cypher command to create a Graph for this project , with the .xml file in the /Prepare/events2xml_results directory.
	
	Before running this Python file, you need to successfully link to neo4j via: 
		- In the terminal, go to the "$NEO4J_HOME/bin" directory and execute the command "neo4j console" first to link the web neo4j database.
		- And you maybe need to change the user name, password and database used in the .py code.
	
- Cypher_Language_Command&Results.pdf: Description, commands and query example results of the cypher language in this project.

- NaCaGraph.db.dump: The exported database.

- Graph_structure(data_model)(schema).svg: Data model of NaCaGraph.db.

- query_scripts.cypher: Cypher script file of query examples, graph visualization for schema and download graph style.

- stylesheet.grass: Graph stylesheet of NaCaGraph.db.
                         
- README.txt: This file.


# Usage:
- Create Graph:
	Option 1: run Create_Graph.py.
	Option 2: $NEO4J_HOME> bin/neo4j-admin load --from=[PATH]/Access/NaCaGraph.db.dump --database=graph.db --force
- Queries:
	Option 1: Enter the commands into the database's editor to run it.
	Option 2: Use query_scripts.cypher.
