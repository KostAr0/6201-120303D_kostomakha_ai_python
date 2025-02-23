import math
import yaml
import os
import matplotlib.pyplot as plt
import sys

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))


def function(x, a, b, c):
    """
    Calculate the value of y for a given x with parameters a, b, and c.
    """
    return a * ((math.e**(2*b*x + c) + 1) / (math.e**(2*b*x + c) - 1))


def read_yaml(file_path):
    """
    Parse YAML file and extract necessary parameters.
    """
    file_path = os.path.join(script_dir, file_path)
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            required_keys = ['xmin', 'step', 'xmax', 'a', 'b', 'c']
            if not all(key in data for key in required_keys):
                raise ValueError("Parameters are missing in the YAML file.")
            return [data[key] for key in required_keys]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format - {e}")
        sys.exit(1)


def write_results(file_path, x_values, y_values):
    """
    Write results to a file in pair format.
    """
    file_path = os.path.join(script_dir, file_path)
    with open(file_path, 'w') as file:
        file.writelines(f"{x} {y}\n" for x, y in zip(x_values, y_values))


def generate_data(xmin, step, xmax, a, b, c):
    """
    Generate x and y values based on the given parameters.
    """
    if step <= 0:
        raise ValueError("Step must be positive.")
    x_values = []
    y_values = []
    x = xmin
    while x <= xmax:
        x_values.append(x)
        y_values.append(function(x, a, b, c))
        x += step
    return x_values, y_values


def plot_data(x_values, y_values):
    """
    Plot the generated data.
    """
    plt.plot(x_values, y_values)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Function Plot')
    plt.show()


def main(xmin, step, xmax, a, b, c):
    """
    Main function to calculate, write, and plot the data.
    """
    x_values, y_values = generate_data(xmin, step, xmax, a, b, c)
    write_results("results.txt", x_values, y_values)
    plot_data(x_values, y_values)


def parse_command_line_args():
    """
    Parse command-line arguments.
    """
    if len(sys.argv) == 7:
        try:
            return map(float, sys.argv[1:])
        except ValueError:
            print("Error: All arguments must be numbers.")
            sys.exit(1)
    else:
        return read_yaml("config.yml")


if __name__ == "__main__":
    params = parse_command_line_args()
    main(*params)