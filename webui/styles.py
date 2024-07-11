# styles.py
css = """
#container {background-color: #f0f0f0;}
.gradio-container {font-size: 14px;}
#top-nav {
    background-color: #333;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
#title {
    font-size: 24px;
    font-weight: bold;
    margin: 0;
    color: white !important;
}
.program-settings, .accessibility-settings {
    background-color: #e0e0e0;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
}
.section-title {
    font-size: 16px;
    margin-bottom: 5px;
    cursor: pointer;
    user-select: none;
    background: none;
    border: none;
    text-align: left;
    padding: 0;
    color: black;
}
.program-settings .gradio-group, .accessibility-settings .gradio-group {
    gap: 5px;
}
#program-table table {
    font-size: 10px !important;
    white-space: nowrap;
    text-overflow: ellipsis;
}
#program-table th {
    font-size: 10px !important;
    white-space: nowrap;
    position: relative;
}
#program-table th.sorting:after,
#program-table th.sorting:before,
#program-table th.sorting_asc:after,
#program-table th.sorting_asc:before,
#program-table th.sorting_desc:after,
#program-table th.sorting_desc:before {
    display: none !important;
}
#program-table td {
    font-size: 9px !important;
    padding: 2px 4px !important;
}
.main-columns {
    display: flex;
    gap: 20px;
}
.left-column {
    flex: 1;
    max-width: 300px;
}
.right-column {
    flex: 3;
}
"""