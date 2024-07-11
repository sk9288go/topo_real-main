import pandas as pd
import logging

MAX_PROGRAMS = 50

class Program:
    def __init__(self, name, area, height, max_floor):
        self.name = name
        self.area = area
        self.height = height
        self.max_floor = max_floor
        self.space_id = None
        self.py = round(area / 3.3058, 2)
        self.vox_amount = round(area * height, 2)
        self.accessibility = {
            'sun_acc': 0.5,
            'ent_acc': 0.5,
            'str_acc': 0.5,
            'ung_pre': 0.5,
            'dist_facade': 0.5,
            'top_pre': 0.5
        }
        self.relationships = {}

programs = []

def add_program(name, area, height, max_floor, sun_acc, ent_acc, str_acc, ung_pre, dist_facade, top_pre):
   
    if len(programs) >= MAX_PROGRAMS:
        logging.warning("Maximum number of programs reached")
        return "Maximum number of programs reached", None, None
    
    program = Program(name, area, height, max_floor)
    program.space_id = len(programs)
    program.accessibility = {
        'sun_acc': sun_acc,
        'ent_acc': ent_acc,
        'str_acc': str_acc,
        'ung_pre': ung_pre,
        'dist_facade': dist_facade,
        'top_pre': top_pre
    }
    programs.append(program)
    
    
    table = update_program_table()
    matrix = update_relationship_matrix()
   
    return f"Added program: {name}", table, matrix


def update_program(index, name, area, height, max_floor, sun_acc, ent_acc, str_acc, ung_pre, dist_facade, top_pre):
    if 0 <= index < len(programs):
        program = programs[index]
        program.name = name
        program.area = area
        program.height = height
        program.max_floor = max_floor
        program.py = round(area / 3.3058, 2)
        program.vox_amount = round(area * height, 2)
        program.accessibility = {
            'sun_acc': sun_acc,
            'ent_acc': ent_acc,
            'str_acc': str_acc,
            'ung_pre': ung_pre,
            'dist_facade': dist_facade,
            'top_pre': top_pre
        }
        return f"Updated program: {name}", update_program_table(), update_relationship_matrix()
    return "Invalid index", None, None

def remove_program(index):
    if 0 <= index < len(programs):
        removed = programs.pop(index)
        for i, program in enumerate(programs):
            program.space_id = i
        return f"Removed program: {removed.name}", update_program_table(), update_relationship_matrix()
    return "Invalid index", None, None

def get_program(index):
    if 0 <= index < len(programs):
        return programs[index]
    return None

def update_program_table():
    data = []
    for program in programs:
        data.append([
            program.name,
            program.space_id,
            program.area,
            program.py,
            program.height,
            program.max_floor,
            program.vox_amount,
            *program.accessibility.values(),
            "X"  # Delete button
        ])
    columns = ["Name", "Space ID", "Area (m²)", "PY", "Height (m)", "Max Floor", "Vox Amount",
               "Sun", "Entrance", "Street", "Underground", "Facade", "Top", "Delete"]
    df = pd.DataFrame(data, columns=columns)
    return df

def update_relationship_matrix():
    matrix = []
    for i, program1 in enumerate(programs):
        row = []
        for j, program2 in enumerate(programs):
            if i == j:
                row.append(1)
            elif i < j:
                row.append(program1.relationships.get(program2.name, 0.5))
            else:
                row.append(program2.relationships.get(program1.name, 0.5))
        matrix.append(row)
    
    return matrix

def update_relationship(data):
    if isinstance(data, dict):
        for i, (row_key, row) in enumerate(data.items()):
            if isinstance(row, dict):
                for j, value in enumerate(row.values()):
                    if i != j and i < len(programs) and j < len(programs):
                        try:
                            float_value = float(value)
                            set_relationship(i, j, float_value)
                        except ValueError:
                            pass  # Ignore non-numeric values
    elif isinstance(data, list):
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                if i != j and i < len(programs) and j < len(programs):
                    try:
                        float_value = float(value)
                        set_relationship(i, j, float_value)
                    except ValueError:
                        pass  # Ignore non-numeric values
    return update_relationship_matrix()

def set_relationship(program1_index, program2_index, value):
    if 0 <= program1_index < len(programs) and 0 <= program2_index < len(programs):
        if program1_index < program2_index:
            programs[program1_index].relationships[programs[program2_index].name] = value
            programs[program2_index].relationships[programs[program1_index].name] = value
        else:
            programs[program2_index].relationships[programs[program1_index].name] = value
            programs[program1_index].relationships[programs[program2_index].name] = value

def get_programs_data():
    return [{'name': p.name, 'id': p.space_id} for p in programs]

def get_relationships_data():
    relationships = []
    for i, p1 in enumerate(programs):
        for j, p2 in enumerate(programs):
            if i < j:
                value = p1.relationships.get(p2.name, 0.5)
                relationships.append({'source': i, 'target': j, 'value': value})
    return relationships

def export_to_excel():
    if not programs:
        return "No programs to export"
    
    program_df = update_program_table()
    relationship_df = pd.DataFrame(update_relationship_matrix(), 
                                   index=[p.name for p in programs],
                                   columns=[p.name for p in programs])
    
    with pd.ExcelWriter("space_planner_export.xlsx") as writer:
        program_df.to_excel(writer, sheet_name="Programs", index=False)
        relationship_df.to_excel(writer, sheet_name="Relationships")
    
    return "Exported to space_planner_export.xlsx"

if __name__ == "__main__":
    logging.info("space_planner_logic module loaded")
