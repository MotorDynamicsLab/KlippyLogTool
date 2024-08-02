if __name__ == "__main__":
    file_path = "./klippy.log"
    result, out_log = extract_config(file_path)
    target_bed, target_extruder = get_last_target_temp(out_log)
    print(target_bed, target_extruder)

    print(get_error_tip(out_log))
    print_stats_lines(file_path)
    # print(result)

    output_file_path = "klipper.cfg"
    with open(output_file_path, "w") as file:
        file.write(result)
