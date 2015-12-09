import gdata.docs.client
import gdata.docs.service

class SampleConfig(object):
    APP_NAME = 'GDataDocumentsListAPISample-v1.0'
    DEBUG = False

client = gdata.docs.client.DocsClient()
client.ClientLogin('doronshai@gmail.com','Ilmbfvm2015','','')

col = gdata.docs.data.Resource(type='folder', title='Folder Name')
col = client.CreateResource(col)

doc = gdata.docs.data.Resource(type='document', title='I did this')
doc = client.CreateResource(doc, collection=col)


# Create a query matching exactly a title, and include collections
q = gdata.docs.client.DocsQuery(
    title='EFD',
    title_exact='true',
    show_collections='true'
)

# Execute the query and get the first entry (if there are name clashes with
# other folders or files, you will have to handle this).
folder = client.GetResources(q=q).entry[0]

# Get the resources in the folder
contents = client.GetResources(uri=folder.content.src)

# Print out the title and the absolute link
for entry in contents.entry:
    print entry.title.text, entry.GetSelfLink().href
