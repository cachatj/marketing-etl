#  #!/usr/bin python

#  Copyright (c) 2020.  Dave Davis
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
""" App that populates a database of paid media platform cost data on three dimensions.
    Account, Campaign and Ad levels."""
import argparse
import time

import fiscalyear

from dg_config.settingsfile import get_settings
import dg_utils.timing
from dg_date import daterange
from dg_db.db_utils import init_db
from dg_google import google_ads_report_builder
from dg_microsoft import microsoft_ads_report_builder

settings = get_settings()


def main(quarter):
    """ Main method that calls all the worker modules """
    print('Tracker Running...')
    print(f"Running for quarter {quarter} ")

    # Truncate and setup database tables with SQLAlchemy
    print('Truncating database tables...')
    init_db()
    print('Tables truncated.')

    # Set date range.
    print('Calculating date range for reports..')

    google_date_range = daterange.get_google_date_range(quarter)
    bing_date_range_start, bing_date_range_end = daterange.get_bing_date_range(quarter)
    print("Google Date Range is: ", google_date_range)
    print("Bing Date Range is: ", bing_date_range_start, bing_date_range_end)

    # Initialize the report retrieval flow. Stagger platforms & sleep for rate limiting.
    google_ads_report_builder.get_report(google_date_range, report_type="accounts")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="accounts")
    # time.sleep(10)
    #
    google_ads_report_builder.get_report(google_date_range, report_type="campaigns")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="campaigns")
    # time.sleep(10)
    #
    google_ads_report_builder.get_report(google_date_range, report_type="ads")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="ads")
    #
    google_ads_report_builder.get_report(google_date_range, report_type="shopping")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="shopping")


if __name__ == "__main__":
    # Set up argparse and support reporting for previous quarter.
    parser = argparse.ArgumentParser(description="Updates or backfills SEM platform reporting.")
    parser.add_argument("-q", "--quarter",
                        type=int,
                        default=fiscalyear.FiscalQuarter.current().quarter,
                        help="The quarter period as an integer. 1, 2, 3 or 4 which will be for the current fiscal year.")
    args = parser.parse_args()

    main(args.quarter)
