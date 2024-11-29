# mergeapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from .utils import merge_files, remove_existing_merged_files
from django.conf import settings

# Place your directories and ignore_sheets dictionaries here
base_path = os.path.join("Reports", "Monthly")

directories = {
    os.path.join(base_path, "IMER"): 8,
    os.path.join(base_path, "MDS"): 9,
    os.path.join(base_path, "PEPFAR_MER_QUARTERLY_MONTHLY"): 8,
    os.path.join(base_path, "PEPFAR_MER_SEMI_ANNUAL_MONTHLY"): 8,
    os.path.join(base_path, "RMDAH"): 9,
    os.path.join(base_path, "RMPREP"): 8,
    os.path.join(base_path, "TPT"): 7,
    os.path.join(base_path, "TX_TB"): 12,
    os.path.join("Reports", "Quarterly", "PEPFAR_MER_QUARTERLY"): 8,
    os.path.join("Reports", "Semi-annual", "PEPFAR_MER_SEMI_ANNUAL"): 8
}

ignore_sheets = {
    os.path.join(base_path, "PEPFAR_MER_QUARTERLY_MONTHLY"): ["PrEP Extra Dissag"],
    os.path.join(base_path, "PEPFAR_MER_SEMI_ANNUAL_MONTHLY"): ["TX_TB"],
    os.path.join("Reports", "Quarterly", "PEPFAR_MER_QUARTERLY"): ["PrEP Extra Dissag"]
}

class MergeFilesView(APIView):
    def post(self, request):
        try:
            for directory, start_row in directories.items():
                # Check if the directory exists, if not, create it
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    print(f"Directory {directory} created.")

                remove_existing_merged_files(directory)
                ignore = ignore_sheets.get(directory, [])
                output_file = os.path.join(directory, "Merged_output.xlsx")
                if directory == os.path.join(base_path, "IMER"):
                    merge_files(directory, 8, ignore, output_file)
                else:
                    merge_files(directory, start_row, ignore, output_file)
            return Response({"message": "Files merged successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
