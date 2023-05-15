def connect_to_grum():
    if not bec.plotter.connected:
        bec.plotter.connect()
    if bec.plotter.connected:
        bec.plotter.select(dev.bpm4i)


def plot_polarisation_difference(data, metadata):
    connect_to_grum()
    _x_motor = metadata["primary"][0]
    _y_selected = bec.plotter._y_selected
    scan_item = bec.queue.scan_storage.current_scan

    if not scan_item:
        scan_item = bec.queue.scan_storage.find_scan_by_ID(metadata["scanID"])

    if not "pol" in metadata:
        return

    if metadata["pol"] == 1:
        if data["point_id"] == 0:
            bec.plotter.new_plot("Difference in polarization, c+ - c-")
            bec.plotter.set_data("Difference in polarization, c+ - c-", [[], []])

    elif metadata["pol"] == -1:
        scan_data = scan_item.data[data["point_id"]].content["data"]
        x = scan_data[_x_motor][_x_motor]["value"]
        y = scan_data[_y_selected][_y_selected]["value"]
        prev_scan_item = bec.queue.scan_storage.storage[-2]
        prev_scan_data = prev_scan_item.data[data["point_id"]].content["data"]
        y_prev = prev_scan_data[_y_selected][_y_selected]["value"]
        y_diff = y_prev - y
        bec.plotter.append_data([x, y_diff])
