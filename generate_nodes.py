import csv, inspect, os, argparse

#Making a lot of nodes and changing properties in the animgraph is hell. especially when you've got 90 nodes and 90 variables
#The intention of this script is to make that suck less for me

PATH = os.path.dirname(__file__)

GRAPH_POSITION = (-10,0)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default=PATH + '\\facemappings.csv')
parser.add_argument('-o', '--output', default="E:\DayZ Projects\DZ\\anims\workspaces\player\player_main\Gestures.agr")
args = parser.parse_args()

def GenerateNodes( path, export ):

    swapaxis = ['Z','X','Y']
    nodes = ""
    vars = ""

    template_gesturegraph = open(PATH+'\Gestures.agr').read()
    template_playermain = open(PATH+'\player_main.agr').read()

    with open( path )as csvfile:
        csvparse = list(csv.reader(csvfile,delimiter=',', quotechar='|'))
        csvparse.pop(0)

        for idx, row in enumerate(csvparse):
            
            for axis_idx, axis in enumerate(('X','Y','Z')):

                bonename = row[0].replace('face_','')
                influence = row[2]

                connectnode = ""
                if (axis_idx > 0): connectnode = f"translate_{bonename}{swapaxis[axis_idx]}"
                elif (idx > 0): connectnode = f"translate_{csvparse[idx-1][0].replace('face_','')}Z"

                varname = row[0].replace('face_','FOIP_') + axis
                var = f"            #VAR {varname} float 0.0 -1.0 1.0 \"\" \n"
                vars += var

                node_string = inspect.cleandoc(f"""
                $Node AnimNodeRot {{ 
                    "translate_{bonename}{axis}" "" "{connectnode}" "FOIP_{bonename}{axis}"
                    $rotitems 1 {{
                        $ri {{
                                "face_{bonename}" "{swapaxis[axis_idx].lower()}lt" {float(influence)}
                        }}
                    }}
                    $EditorData {{
                        #EditorPos {GRAPH_POSITION[0]+(2.5*axis_idx)}, {GRAPH_POSITION[1]+(.75*idx)}
                    }}
                }}
                """)

                nodes += f"\n{node_string}\n"

    final = template_gesturegraph.replace('//[replacednodes]',nodes)
    finalvars = template_playermain.replace('//[facevars]',vars)

    f = open(export, "w")
    f.write(final)

    f = open('E:\DayZ Projects\DZ\\anims\workspaces\player\player_main\player_main.agr',"w")
    f.write(finalvars)


GenerateNodes(args.input,args.output)
print(f"exported nodes to: {args.output}")
