# 1. 임포트 문을 수정합니다.
from space_planner_logic import *  # 상대 임포트 제거

import gradio as gr
import json
from styles import css
from graph import js
import traceback

import os  # os 모듈 추가
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)


import sys


try:
    from space_planner_logic import *
except ImportError as e:
    sys.exit(1)

with gr.Blocks(css=css, js=js) as demo:
    settings_open = gr.State(True)
    accessibility_open = gr.State(True)
    current_program_index = gr.State(None)

    with gr.Row(elem_id="top-nav"):
        gr.HTML("<h1 id='title'>Space Planner</h1>")
    
    with gr.Row(elem_classes="main-columns"):
        with gr.Column(elem_classes="left-column"):
            with gr.Group(elem_classes="program-settings"):
                settings_title = gr.Button("▼ Program Settings", elem_classes="section-title")
                with gr.Group() as settings_content:
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Program Name", elem_classes="setting-label")
                        name_input = gr.Textbox(container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Area (m²)", elem_classes="setting-label")
                        area_input = gr.Number(container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Height (m)", elem_classes="setting-label")
                        height_input = gr.Number(container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Max Floor", elem_classes="setting-label")
                        max_floor_input = gr.Number(container=False, elem_classes="setting-input")

            with gr.Group(elem_classes="accessibility-settings"):
                accessibility_title = gr.Button("▼ Accessibility Settings", elem_classes="section-title")
                with gr.Group() as accessibility_content:
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Sun Accessibility", elem_classes="setting-label")
                        sun_acc = gr.Slider(0, 1, value=0.5, container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Entrance Accessibility", elem_classes="setting-label")
                        ent_acc = gr.Slider(0, 1, value=0.5, container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Street Accessibility", elem_classes="setting-label")
                        str_acc = gr.Slider(0, 1, value=0.5, container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Underground Preference", elem_classes="setting-label")
                        ung_pre = gr.Slider(0, 1, value=0.5, container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Distance from Facade", elem_classes="setting-label")
                        dist_facade = gr.Slider(0, 1, value=0.5, container=False, elem_classes="setting-input")
                    with gr.Row(elem_classes="setting-row"):
                        gr.Markdown("Top Preference", elem_classes="setting-label")
                        top_pre = gr.Slider(0, 1, value=0.5, container=False, elem_classes="setting-input")

            add_btn = gr.Button("Add Program")
            update_btn = gr.Button("Update Program", visible=False)
        
        with gr.Column(elem_classes="right-column"):
            gr.Markdown("### Programs")
            program_table = gr.Dataframe(
                headers=["Name", "Space ID", "Area (m²)", "Py (평)", "Height (m)", "Max Floor", 
                        "Vox Amount", "Sun", "Entrance", "Street", "Underground", "Facade", "Top", "Delete"],
                col_count=(14, "fixed"),
                height=300,
                elem_id="program-table"
            )
        
            gr.Markdown("### Program Relationships")
            relationship_graph = gr.HTML('<div id="relationship-graph"></div>')

    
    with gr.Row():
        export_btn = gr.Button("Export to Excel")
        output = gr.Textbox(label="Output")
    
    def toggle_settings(is_open):
        return (
            not is_open,
            gr.update(visible=not is_open),
            gr.update(value="▼ Program Settings" if not is_open else "▶ Program Settings")
        )

    def toggle_accessibility(is_open):
        return (
            not is_open,
            gr.update(visible=not is_open),
            gr.update(value="▼ Accessibility Settings" if not is_open else "▶ Accessibility Settings")
        )

    settings_title.click(
        toggle_settings,
        inputs=[settings_open],
        outputs=[settings_open, settings_content, settings_title]
    )
    
    accessibility_title.click(
        toggle_accessibility,
        inputs=[accessibility_open],
        outputs=[accessibility_open, accessibility_content, accessibility_title]
    )

    def add_program_wrapper(*args):
       
        try:
          
            result = add_program(*args)
            if result[1] is None:               
                return "Failed to add program", None, gr.update(value="<div>Failed to add program</div>"), gr.update(visible=True), gr.update(visible=False)
            programs_data = get_programs_data()
            relationships_data = get_relationships_data()
           
            graph_data = {
                'programs': programs_data,
                'relationships': relationships_data
            }
            graph_json = json.dumps(graph_data)
            graph_html = f'<div id="graph-data" style="display:none;">{graph_json}</div><script>updateGraph({graph_json});</script>'
            return (
                result[0],
                result[1],
                gr.update(value=graph_html),
                gr.update(visible=True),
                gr.update(visible=False)
            )
        except Exception as e:
            logger.error(f"Error in add_program_wrapper: {str(e)}")
            logger.error(traceback.format_exc())
            return (
                f"Error: {str(e)}",
                None,
                gr.update(value="<div>Error occurred</div>"),
                gr.update(visible=True),
                gr.update(visible=False)
            )

    add_btn.click(
    add_program_wrapper,
    inputs=[name_input, area_input, height_input, max_floor_input, sun_acc, ent_acc, str_acc, ung_pre, dist_facade, top_pre],
    outputs=[output, program_table, relationship_graph, add_btn, update_btn]
    )
  
    def update_relationships(matrix):
        update_relationship_matrix(matrix)
        return "Relationships updated"

    demo.load(fn=None, inputs=None, outputs=None)

        # Initialize graph
    gr.HTML('<script>initGraph();</script>')

if __name__ == "__main__":
    demo.launch(debug=True)
else:
    demo.queue()