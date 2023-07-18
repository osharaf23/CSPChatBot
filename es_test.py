
import os
import openai
import csv
import sys
import pandas as pd
from datetime import date
# import panel as pn  # GUI

from elasticsearch import Elasticsearch, RequestsHttpConnection

clusters = {
    "common_2": "https://vpc-poseidon-env2-2-kw7hnzhzzgkqlxznkbqdgvjt7i.us-east-1.es.amazonaws.com"
    }


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# app_id = 'WJ6GRX-JV79T7R849'

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def collect_messages(new_message):
    messages.append({'role':'user', 'content':f"{new_message}"})
    response = get_completion_from_messages(messages) 
    messages.append({'role':'assistant', 'content':f"{response}"})

    return response
 


mapping = """
"mappings" : {
      "dynamic_templates" : [
        {
          "strings" : {
            "match_mapping_type" : "string"
          }
        }
      ],
      "properties" : {
        "_storage_id",
        "app_category",
        "app_id",
        "app_name",
        "app_vendor",
        "confidence",
        "country",
        "device_country",
        "device_name",
        "device_region",
        "domain_category",
        "domains",
        "endpoint_groups",
        "event_date",
        "expiration",
        "expiry_time",
        "mac_address",
        "network",
        "os_version",
        "pid",
        "pname",
        "policy_action",
        "policy_id",
        "policy_name",
        "qip",
        "qname",
        "qtype",
        "query_type",
        "rcode",
        "refined_at",
        "response",
        "response_country",
        "response_region",
        "rip",
        "severity",
        "sld",
        "source",
        "storage_id",
        "tclass",
        "tfamily",
        "timestamp",
        "tproperty",
        "type",
        "user"
      }
    }
"""

descriptions = """
"_storage_id": "string value of storage id" \
"app_category": "The different categories a given app can fit into. Options are Platform as a Service (PaaS), Search Engines, Communication, \
Business App Suite, Security, Information Technology, Email, Cloud Backup and Storage, Content Delivery Network (CDN), Consumer Services"\
"app_id": "The id of a given app"\
"app_name": "The name of a given application"\
"app_vendor": "Vendor of the given app"\
"confidence": "Refers to the trustworthiness associated with the response received from the DNS server."\
"country": "country of origin of a DNS query"\
"device_country": "the country where the device sending the DNS query is located"\
"device_name": "name of the device that sent the query. Can be either the B1EP device name or IP metadata coming from a data connector or qip if nothing else is available." \
"device_region": "region where the device sending the DNS query is located"\
"domain_category": "What category the domain of origin can be placed into" \
"domains": "flattened nested domains from the qname" \
"endpoint_groups": "Sets or categories of DNS resolvers or serviers that can be used to process the query."\
"event_date": "date and time the query was sent. format is yyyy-MM-dd'T'HH:mm:ss.SSSZ"\
"expiration": "The TTL (time to live) which refers to how long the query will remain in the cache. after this time, the client must send the query again."\
"expiry_times": "same as expiration"\
"mac_address": "The MAC address of the device sending the DNS query. This is the identifier a given device."\
"network": "The network through which the query is sent from the client to the DNS server" \
"os_version": "The operating system the device sending the DNS query was operating on" \
"pid": "the policy identifier"\
"pname": "Product name"\
"policy_action": "The action the DNS server has chosen to take towards the query. Can eiher be "Allow", "Block", "Log", or "Redirect"."\
"policy_id": "string value of the policy ID"\
"policy_name": "name of the policy enacted"\
"qip": "the IP address of the requester or client sending the DNS query"\
"qname": "DNS query name in FQDN(fully qualified domain name, meaning the exact location in the tree hierarchy of the domain name system)" \
"qtype": "the decimal representation of the id corresponding to "query_type". 1 = "A", 255 = "*", 65 = "HTTPS", 28 = "AAAA", 16 = "TXT", 12 = "PTR", \
64 = "SVCB", 5 = "", 2 = "NS", 33 = "SRV". " \
"query_type": "These are the equivalent of DNS records created to provide important information about a domain or hostname, particularly its current IP address. \
A = DNS host record, stores a hostname and its corresponding IPv4 address, AAAA = stores a hostname and its corresponding IPv6 address, CNAME = used to alias \
a hostname with another hostname, MX = specifies an SMTP email server for the domain used to route outgoing emails to an email server, NS = specifies that a DNS \
zone is delegated to a specific Authoritative Name Server and provides the address of the name server, PTR = allows a DNS resolver to provide an IP address \
and receive a hostname, CERT = stores encryption certificates, SRV = a service location record, like MX but for other communication protocols, TXT = carries machine \
readable data, SOA = indicates the Authoritative Name Server for the currect DNS zone, contact details for the domain administrator, domain serial number \
and information on how frequently DNS informaton for this zone should be refreshed, HTTPS = "\
"rcode": "messages that indicate the response of the DNS query. possible values are 0, 1, 2, 3, 4, 5, 6, 7, 8, 9. 0 = QNS Query completed successfully, 1 = DNS Query Format Error, \
2 = server failed to complete the DNS reques, 3 = Domain name does not exist, 4 = Function not implemented, 5 = The server refused to \
answer for the query, 6 = Name that should not exist does not exist, 7 = RRset should not exist does not exist, 8 = server not authoritative \
for the zone, 9 = Name not in zone"\
"refined_at": "the time the DNS query was refined"\
"response": "the response sent back to the client from the DNS server in response to the DNS query. Can correspond to a given rcode as well. \
"NXDOMAIN" = rcode 3, "NOERROR" = rcode 0, "NOTIMP" = rcode 4, "REFUSED"= rcode 5. If the response type cannot be found here refer back to the "rcode" field."\
"response_country": "country the response originates from"\
"response_region": "region the response originates from"\
"rip": "Responder IP address (where the response originates from)"\
"severity": "the severity of the risk associated with the DNS query"\
"sld": "second level domain"\
"source": "can be either the data source or the DNS server ID"\
"storage_id": "storage id"\
"tclass": "threat class"\
"tfamily": "threat family"\
"timestamp": "epoch value"\
"tproperty": "similar to tfamily"\
"type": "the type of the data that is returned"\
"user": "User name of the client that submitted the DNS query" 
"""

examples = """
"Gets possible values for the <pname> field": "{"size": 0,"aggs": {"distinct_values": {"terms": {"field": "pname"}}}}", \
"Gets possible values for the <query_type> field": "{"size": 0,"aggs": {"distinct_values": {"terms": {"field": "query_type"}}}}", \
"How many queries came from emails?": "{"track_total_hits": true,"query": {"match": {"query_type": "MX"}}}", \
"What kinds of queries came in over the past 2 days?" : "{"query": {"bool": {"filter": [{"range": {"event_date": {"gte": "2023-07-06T00:00:00.000Z","lte": "2023-07-08T23:59:59.999Z"}}}]}},"size": 0,"aggs": {"unique_users": {"terms": {"field": "qtype"}}}}", \
"What are the three most common types of queries that came in over the past 2 days?" : "{"query": {"bool": {"filter": [{"range": {"event_date": {"gte": "2023-07-06T00:00:00.000Z","lte": "2023-07-08T23:59:59.999Z"}}}]}},"size": 0,"aggs": {"unique_users": {"terms": {"field": "qtype","size":3}}}}", \
"Which product had the most queries in the past 10 days?" : "{"size": 0, "aggs": {"top_product": {"terms": {"field": "pname", "size": 1, "order": {"_count": "desc"}}}}, "query": {"range": {"event_date": {"gte": "2023-06-30T00:00:00.000Z", "lte": "2023-07-10T23:59:59.999Z"}}}}", \
"What are the top 3 most frequent device type in my network?" : "{"size": 0, "aggs": {"top_devices": {"terms": {"field": "device_name", "size": 3, "order": {"_count": "desc"}}}}}", \
"What domain is currently providing the most NXDOMAIN responses on the network?" : "{"size": 0,"query": {"match": { "response": "NXDOMAIN"}},"aggs": {"devices": {"terms": {"field": "domains","size": 1}}}}", \
"What is the most frequent domain category?" : "{"size": 0, "aggs": {"top_domain_category": {"terms": {"field": "domain_category", "size": 1, "order": {"_count": "desc"}}}}}"
"""

today = date.today()

content = """
"You are a chatbot designed to output Elastic Search queriess based in natural language \
prompts given by a user. Here are instructions to follow in order to do this successfully. Make sure \
you read through every step before constructing your query to ensure you are following the steps correctly. \

1. Use the descriptions of what information is stored in each Elastic Search index deliminated by triple \
brackets [[["""+ descriptions +"""]]] to know what dields are present in each Elastic Search index and to understand \
what information is stored in each field. When accessing a field in the elastic search index, make sure the field name \
you are passing through matches exactly to one of the names listed in descriptions with nothing additional added. \
2. When passing in a field name in the "field"" category when doing aggregations fo queries, make sure you only pass the string value \
of the field name you want without anything else. There are no subfields so please do not add anything else. For example, do not include ".keyword" \
at the end of the field name. \
3. Today's date is """ + str(today) + """ which you should use if the user inputs a prompt \
that is dependent on the date. The "event_date" field is formatted as "yyyy-MM-dd'T'HH:mm:ss.SSSZ" \
so when specifying dates in your query please match this format. \
4. There are some common queries you may be asked and it is best to know what the expected return type is. \
If the user asks a prompt including "how much", "how many", or other verbiage that indicates they want to know \
the quantity of something, please output a number reflecting the quantity of whatever they are searching for.\
5. If the user asks a prompt including "what kind", "who", or other verbiage that indicates they want to know \
what values fall meet their criteria or fall into a certain category, please output a list of these values.\
6. If the user asks a prompt including "When", "from which dates", or other verbiage that indicates they want to know \
the timeframe an event or events happened in, please output the date or dates that match their criteria. \
7. The query code should return only the answer the customer is looking for and no extra information. \
8. You should reference this set of examples deliminated by triple angle brackets <<<""" + examples + """>>> that \
show examples of possible queries for a given prompt. Search this to find examples of prompts similar to the one inputted by \
the user and use the corresponding query to help you structure yours. \

Make sure you address all parts of the user's inputted prompt before returning the query.\

Return the json code part of the answer, as well as a some text explaining how you decided on the query you returned. Compress the json output removing spaces and output only this compressed json script" \
"""

messages = [{'role':'system', 'content': content}]

def collect_messages(new_message):
    messages.append({'role':'user', 'content':f"{new_message}"})
    response = get_completion_from_messages(messages) 
    messages.append({'role':'assistant', 'content':f"{response}"})

    return response

def test(prompt):
  results = []
  results.append(prompt)

  query_body = collect_messages(prompt)
  # print(query_body+"\n\n\n")

  results.append(query_body)

  # prompt for translating ES output into something human readable
  content2 = """
  "You are a chatbot designed to take in a json string that is the output of an elastic search query and translate it into a human readable value. \
  You must figure out what output type (for example, an integer, a string, a list of strings, etc.) the user is looking for based on the query \
  deliminated by triple brackets [[["""+ prompt +"""]]] and then find where this information is located in the inputted json string and output \
  that information.
  """
  context2 = {'role':'system', 'content': content2}

  # queries ES w the LLM outputted query
  for key in clusters:
    host = clusters[key]
    es = Elasticsearch(
        hosts=host,
        use_ssl=False,
        connection_class=RequestsHttpConnection)
    res = es.search(index="poseidon-common-*", body=query_body, request_timeout=3000)
    messages2 = [context2, {'role':'user', 'content': str(res)}]
    human_readable = get_completion_from_messages(messages2 )

    results.append(str(res))
    results.append(human_readable)

    # print(str(res)+"\n\n\n")
    # print(human_readable)
    print(results)

    return results

def save_to_csv(data, filename):
  with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

  print(f"Data saved to {filename}.")

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])

# def run_message(message):
#   test = [context, {'role':'user', 'content':message}]
#   return get_completion_from_messages(test, temperature=0)

# def run_prompt(test_queries):
#   pass

# query_body = {
#     "size": 10,
#     "query": {
#         "match_all": {}
#     }
# }
# for key in clusters:
#     host = clusters[key]
#     es = Elasticsearch(
#         hosts=host,
#         use_ssl=False,
#         connection_class=RequestsHttpConnection)
#     res = es.search(index="poseidon-common-*", body=query_body, request_timeout=3000)
#     print(res)

#### USING GUI ####

# def collect_messages(_):
#     prompt = inp.value_input
#     inp.value = ''
#     context.append({'role':'user', 'content':f"{prompt}"})
#     response = get_completion_from_messages(context) 
#     context.append({'role':'assistant', 'content':f"{response}"})
#     panels.append(
#         pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
#     panels.append(
#         pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
#     return pn.Column(*panels)


# pn.extension()

# panels = [] # collect display 

# inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
# button_conversation = pn.widgets.Button(name="Chat!")

# interactive_conversation = pn.bind(collect_messages, button_conversation)

# dashboard = pn.Column(
#     inp,
#     pn.Row(button_conversation),
#     pn.panel(interactive_conversation, loading_indicator=True, height=300),
# )

# dashboard

