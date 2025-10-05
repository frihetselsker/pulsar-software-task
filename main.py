import argparse
import draw
import search

def main(path):
    r = draw.prepare_image(path)
    height_map = search.prepare_weights(r)
    src = (1, 1)
    dest = (99, 0)
    paths = search.a_star(height_map, src, dest)
    print(paths)
    if paths is not None:
        draw.draw_path(paths)

 
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the shortest path to an object for a rover")
    parser.add_argument("--path", type=str, required=True, help="Path to the map")

    args = parser.parse_args()
        
    main(args.path)
