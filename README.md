# Amber_Helen

**Title:** Find Your Ideal PhD Supervisor

**Purpose:** Helps future PhD students find their ideal PhD supervisor by giving them an idea of who are prominent figures
in the specific fields/keywords students are interested in, what schools they are from, what generally what fields the schools
the students are interested in have lots of works in

**Demo:** //TODO: Give the link to your video demo.

**Installation:** N/A - only used the given dataset.

**Usage by widget:**

- **Find University Top Keywords** - search institution you are interested in (must be full name spelled correctly). The widget will load a pie chart depicting
  the specified school's top 10 keywords determined by both count and relevance score

- **Find Faculty Best Keywords** - search a keyword (must be full keyword and spelled correctly). The widget will display the top 5 faculty ordered by the number of
  pappers they have published with the specified keyword. Contact information, pictures, position title, institution, and number of papers
  published with the keyword will be displayed.

- **Fix Missing Faculty Fields** - search a faculty member up by name (can be first name, last name, or full name). The widget will display a table with relevant information
  (name, institution, position, email, phone, and photoUrl) on the matching faculty members with that name. Users can then click on a field
  in that data table and input the appropriate data to fill in any missing fields and update the database backend.

- **Add New Faculty Members** - fill in fields and submit to add a new faculty member that newly joined an institution. The widget will update the backend database to create
  a new faculty member with the appropriate fields

- **Top Publications in Research Interest** - search

- **Trending Keywords by Institution** - search a keyword (choose from dropdown). The widget will display a stacked bar chart with the x-axis being the most recent
  5 years and the y-axis being the number of papers published in that year with the specified keyword. The bars will be broken down by
  institution (i.e. a school with 20 papers in data mining will have a larger stacked component than a school with 5 papers in data mining)

- **Design:** What is the design of the application? Overall architecture and components. //TODO: Write out once all widgets are integrated

**Implementation:** We implemented these widgets using Dash and supporting dash component libaries such as _Dash Mantine Components_, _Dash Core Components_, and _Dash Bootstrap Components_, etc. We also used pandas dataframes to store retrieved data from the databases. The _Dash Bootstrap Components_ were especially helpful in providing Cards that cleanly segemented each widget into logical partitions.

**Database Techniques:** Techniques we implemented included indexing in both MySQL and Neo4j, where we created indexes for specific fields we access the most often (aside from table ids that are already indexed by being PRIMARY KEYs). We also implemented triggers and exceptions. (//TODO: Explain how?)

**Extra-Credit Capabilities:** Fix Missing Faculty Fields Widget offers quick and easy data cleaning by giving users the ability to fill in missing faculty information or fix erroneous data - the multiple input fields and extra data table update after fixing data had to be implemented with extra effort since Dash DataTables currently do not support inline editing of tables with strings (although they do with numbers - we had to learn through bug forums) and handling updating the same output with multiple inputs through advanced callbacks with dash.callback_context.

**Contributions:**
Helen:

1. Tasks done:
   Widgets - Find University Top Keywords, Find Faculty Best Keywords, Fix Missing Faculty Fields
   Techniques - Indexing
   Databases used - MySQL and Neo4j
   Misc. - created repository, project outline/plan, widget brainstorming, wrote out README file

2. Estimated time spent: 30 hours

Amber:

1. Tasks done:
   Widgets - Add New Faculty Members, Top Publications in Research Interest, Trending Keywords by Institution
   Techniques - Triggers, Exceptions
   Databases used - MySQL and MongoDB
   Misc. - project outline/plan population, widget brainstorming

2. Estimated time spent: 30 hours
