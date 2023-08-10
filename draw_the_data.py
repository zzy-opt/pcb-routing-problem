from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import Polygon


class DrawData:


    case = '03.303'
    folder = 'usecase/' + case + "/"
    layout_path = folder + 'layout.txt'
    pin_path = folder + 'pin.txt'


    def main(self):
        unique_layers = self.get_unique_layer(self.pin_path)

        layer_map = {i: plt.subplots() for i in unique_layers}
        for i in unique_layers:
            layer_map[i][0].set_dpi(900)
            self.add_layout_file(layer_map[i][1],self.layout_path)

        with open(self.pin_path, 'r') as pin_file:
            line = pin_file.readline()
            while line:
                self.add_rectangle_to_layer_map(layer_map,line)
                self.add_rectangle_index_to_layer_map(layer_map,line)
                line = pin_file.readline()

        # Show the plot
        plt.show()



    def get_unique_layer(self, pin_path):
        # Open the file for reading
        with open(pin_path, 'r') as file:
            # Create a set to store the unique values
            unique_values = set()
            # Read each line of the file
            for line in file:
                # Split the line by spaces
                data = line.split()
                # Get the value in the second column
                value = data[1]
                # Add the value to the set of unique values
                unique_values.add(value)
        # Return the set of unique values
        return unique_values


    def add_rectangle(self, ax, center, length, width):
        # Compute the bottom-left vertex of the rectangle
        x = center[0] - length / 2
        y = center[1] - width / 2

        # Create a Rectangle object
        rect = Rectangle((x, y), length, width, facecolor='red')

        # Add the Rectangle to the Axes
        ax.add_patch(rect)


    def add_layout(self, ax, coordinates):
        # Create a polygon from the given vertices
        polygon = Polygon(coordinates)

        # Get the x and y coordinates of the polygon's exterior
        x, y = polygon.exterior.xy

        # Plot the polygon
        ax.plot(x, y)


    def add_layout_file(self, ax, layout_path):
        # Open the file for reading
        with open(layout_path, 'r') as file:
            # Read the first three lines of the file
            lines = [next(file) for _ in range(3)]
            # Get the third line
            third_line = lines[2]
            # Split the third line by white space
            coordinate_strs = third_line.split()
            coordinates = [tuple(map(float, x.split(','))) for x in coordinate_strs]
            self.add_layout(ax, coordinates)

    def add_rectangle_to_layer_map(self,layer_map,pin_line):
        pin_data = pin_line.split(' ')
        self.add_rectangle(layer_map[pin_data[1]][1],[float(pin_data[2]),float(pin_data[3])],float(pin_data[4]),float(pin_data[5]))

    def add_rectangle_index_to_layer_map(self,layer_map,pin_line):
        pin_data = pin_line.split(' ')
        ax = layer_map[pin_data[1]][1]
        ax.text(float(pin_data[2]),float(pin_data[3]), pin_data[0], color='blue', ha='center', va='center', fontsize=5)

if __name__ == "__main__":
    test = DrawData()
    test.main()
