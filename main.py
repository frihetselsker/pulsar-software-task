import argparse
import draw
import search

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the shortest path to an object for a rover")
    parser.add_argument("--path", type=str, required=True, help="Path to the map image")
    parser.add_argument("--src", type=int, required=False, default=[1, 1], nargs=2, help="Source point coordinates as 'x y' (x = horizontal, y = vertical, default = '1 1')")
    parser.add_argument("--dest", type=int, required=True, nargs=2, help="Destination point coordinates as 'x y' (x = horizontal, y = vertical, default = '1 1')")
    parser.add_argument("--diagonal", action="store_true", help="Allows diagonal movements")
    args = parser.parse_args()
        
    r = draw.prepare_image(args.path)
    height_map = search.prepare_weights(r)
    src = (args.src[1], args.src[0])
    dest = (args.dest[1], args.dest[0])
    paths = search.a_star(height_map, src, dest, args.diagonal)
    if paths is not None:
        draw.draw_path(paths)
