import bpy

# Get the object
obj = bpy.data.objects['face']

# Ensure the object is a mesh
if obj.type == 'MESH':
    
    
    active_shape_key = obj.active_shape_key
    # Get the vertex group named "Order"
    group_index = obj.vertex_groups["Order"].index

    #### Print out the basis vertex positions ##########################################################
    # Get the vertices and their weights in the group
    basis_vertices_and_weights = [(vertex, obj.vertex_groups["Order"].weight(vertex.index)) 
                            for vertex in obj.data.vertices 
                            if obj.vertex_groups["Order"].index in [group.group for group in vertex.groups]]
    # Sort by weight
    basis_vertices_and_weights.sort(key=lambda vw: vw[1])
    # Get their positions and round to 3 decimal places
    basis_positions = [(round(vw[0].co.x, 3), round(vw[0].co.z, 3)) for vw in basis_vertices_and_weights]
    print(f"points_basis = {basis_positions}")

    #### Print out each shape keys' relative vertex positions ###########################################
    for key in obj.data.shape_keys.key_blocks:
        if key.name == "basis": 
            continue
        vertices_and_weights = []
        # Loop through each vertex in the object's data
        for i in range(len(obj.data.vertices)):
            vertex = obj.data.vertices[i]
            shape_key_coord = key.data[i]
            # For each vertex, get the groups it belongs to
            vertex_groups = vertex.groups

            # Initialize a list to store the indices of the groups the vertex belongs to
            group_indices = []

            # Loop through the vertex groups and add their indices to the list
            for group in vertex_groups:
                group_indices.append(group.group)

            # Check if the "Order" group's index is in the list of group indices
            if obj.vertex_groups["Order"].index in group_indices:
                # If it is, get the weight of the vertex in the "Order" group
                weight = obj.vertex_groups["Order"].weight(vertex.index)

                # Add the vertex and its weight to the list
                vertices_and_weights.append((shape_key_coord, weight)) # <<< HERE
        # Sort by weight
        vertices_and_weights.sort(key=lambda vw: vw[1])
        # Get their positions and round to 3 decimal places
        positions = [(round(vw[0].co.x, 3), round(vw[0].co.z, 3)) for vw in vertices_and_weights]
        #print(f"points_{key.name} = {positions}")
        # Find the difference between it and the basis
        difference = [(a[0]-b[0], a[1]-b[1]) for a, b in zip(positions, basis_positions)]
        difference_rounded = [(round(x[0], 3), round(x[1], 3)) for x in difference]
        print(f"relative_points_{key.name} = {difference_rounded}")
else:
    print("Object is not a mesh.")