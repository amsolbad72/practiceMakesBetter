from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from database import (
    create_database,
    add_new_bench,
    get_all_benches_from_database,
    update_bench_availability_status,
    find_specific_bench_by_id
)

web_application = Flask(__name__)
create_database()
print("✅ Database ready!")

@web_application.route('/')
def show_home_page():
    """
    This is our home page route.
    When someone visits our website, this function runs!
    It's like the front door of our house.
    """
    print("👤 Someone visited our homepage!")
    return render_template('index.html')

@web_application.route('/map')
def show_map_page():
    """
    This route shows our interactive map with all the benches.
    It's like opening a treasure map showing all bench locations!
    """
    print("🗺️ Someone wants to see the map!")

    all_benches_list = get_all_benches_from_database()
    benches_for_map = []
    for single_bench in all_benches_list:
        bench_information = {
            'id': single_bench[0],
            'latitude': single_bench[1],
            'longitude': single_bench[2],
            'description': single_bench[3],
            'is_available': single_bench[4],
            'last_updated': single_bench[5],
            'added_by': single_bench[6]
        }
        benches_for_map.append(bench_information)
    print(f"📊 Sending {len(benches_for_map)} benches to map")
    return render_template('map.html', benches=benches_for_map)
