# Amber_Helen

**Title:** Find Your Ideal PhD Supervisor

**Purpose:** Helps future PhD students find their ideal PhD supervisor by giving them an idea of who are prominent figures
in the specific fields/keywords students are interested in, what schools they are from, which universities specialize in which fields.

**Demo:** //TODO: Give the link to your video demo.

**Installation:** Please run the following MySQL commands in the academicworld database:

1. Run the contents in the provided FacultyUniversityView.sql file - this will create a view later referenced
2. Run the contents in the provided GetPublicationsByKeywordAndUniversity.sql file - this will create a stored procedure referencing the aforementioned view
3. Run the contents in the provided FacUniViewAbr.sql file - this will create a view later referenced
4. Run the contents in the provided GetTopUniversitiesByYear.sql file - this will create a stored procedure referencing the aforementioned view

**Usage by widget:**

- **Find University Top Keywords** - search institution you are interested in (must be full name spelled correctly). The widget will load a pie chart depicting
  the specified school's top 10 keywords determined by both count and relevance score.

- **Find Faculty Best Keywords** - search a keyword (must be full keyword and spelled correctly). The widget will display the top 5 faculty ordered by the number of
  papers they have published with the specified keyword. Contact information, pictures, position title, institution, and number of papers
  published with the keyword will be displayed.

- **Fix Missing Faculty Fields** - search a faculty member by name (can be first name, last name, or full name). The widget will display a table with relevant information
  (name, institution, position, email, phone, and photoUrl) on the matching faculty members with that name. Users can then click on a field
  in that data table and input the appropriate data to fill in any missing fields and update the database backend.

- **Add New Database Entries** - add new faculty members or new publications to the database. Choose between faculty and publications. The widget will dynamically display fields appropriate to the user's choice. Fill in fields and submit to add a newly published publication or a faculty member that recently joined an institution. The widget will update the backend database to create a new publication or faculty member with the appropriate fields. (It assumes a user updating the database will not have keywords or keyword scores for faculty or publications.)

- **Top Publications in Research Interest** - find the best publications published on a subject by a chosen institution. Search and choose an area of research and an institution from the dropdowns. The widget will display a table of the top 10 publications on that subject from the user's chosen institution as determined by relevance scores.

- **Trending Research by Institution** - search and choose an area of research from the dropdown. The widget will display a stacked bar chart with the x-axis being the most recent 10 years and the y-axis being the number of papers published in that year with the specified keyword. The bars will be broken down by institution (i.e. a school with 20 papers in data mining will have a larger stacked component than a school with 5 papers in data mining).

**Design:** - We designed this dashboard to have 6 widgets laid out with plenty of space and large fonts for accessiblity. Some widgets dynamically change in height with user input. Starting from the top left, a student can first find universities they are interested in and see what keywords those universities have the most relevance in. Then moving right to the top middle widget, a potential PhD student can find the top publications for the universities they found suited them for the keywords they are interested in. Then moving to the right again to the long right side widget, students can find the top faculty publishing the most papers in the field they are interested in and find their pictures, affiliated institutions, and contact information. Then moving back to the left most widget in the second row, here students can add any faculty missing or new faculty that joined an institution, or even add new publications a faculty might have published more recently. Then the center widget in the second row allows for students to check out the overall trends of a keyword over the most recent publications in the last 5 years recorded in the database. The stacked bar graph will show total number of publications pertaining to the searched keyword and break each bar down by university (i.e. the quantity of papers is grouped by university). Finally, if a student sees anything displayed in the faculty search widget that they would like to fix, such as a missing field, they can use the last widget at the very bottom to update those fields through searching by faculty name and selecting the field they would like to replace.

**Implementation:** We implemented these widgets using Dash and supporting Dash component libaries such as _Dash Mantine Components_, _Dash Core Components_, _Dash Bootstrap Components_, _Dash DataTable_, _Plotly_, etc. We also used pandas dataframes to store retrieved data from the databases. The _Dash Bootstrap Components_ were especially helpful in providing Cards that cleanly segemented each widget into logical partitions.

**Database Techniques:** Techniques we implemented included indexing in both MySQL and Neo4j, where we created indexes for specific fields we access most often (aside from table ids that are already indexed by being PRIMARY KEYs). We implemented views and stored procedures in MySQL by writing the code and implementing it in both of our local databases. Views were helpful in creating virtual tables that were easier to query without using joins repetitively. Stored procedures were helpful for saving actions that needed to be done repetitively in order to get resulting tables that could be uniquely manipulated according to the current needs of the widget.

**Extra-Credit Capabilities:** Fix Missing Faculty Fields Widget offers quick and easy data cleaning by giving users the ability to fill in missing faculty information or fix erroneous data - the multiple input fields and extra data table update after fixing data had to be implemented with extra effort since Dash DataTables currently do not support inline editing of tables with strings (although they do with numbers - we had to learn through bug forums) and handling updating the same output with multiple inputs through advanced callbacks with dash.callback_context.

**Contributions:**
Helen:

1. Tasks done:
   Widgets - Find University Top Keywords, Find Faculty Best Keywords, Fix Missing Faculty Fields
   Techniques - Indexing
   Databases used - MySQL and Neo4j
   Misc. - project outline/plan, widget brainstorming, README file, widget integration

2. Estimated time spent: 30 hours

Amber:

1. Tasks done:
   Widgets - Add New Faculty Members, Top Publications in Research Interest, Trending Research by Institution
   Techniques - Views, Stored Procedures
   Databases used - MySQL and MongoDB
   Misc. - project outline/plan population, contributed to README file, widget brainstorming

2. Estimated time spent: 30 hours
