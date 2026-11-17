
import csv
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from .models import ReconciliationRecord


def upload_transactions(request):

    if request.method == "POST":

        bank_file = request.FILES.get("bank_file")
        internal_file = request.FILES.get("internal_file")

        if not bank_file or not internal_file:
            return render(request, "reconciliation/upload.html", {
                "error": "Please upload both CSV files."
            })

        try:
            bank_df = pd.read_csv(bank_file)
            internal_df = pd.read_csv(internal_file)

            required_columns = {"transaction_id", "amount"}

            if not required_columns.issubset(bank_df.columns):
                raise ValueError(
                    "Bank CSV must contain transaction_id and amount columns."
                )

            if not required_columns.issubset(internal_df.columns):
                raise ValueError(
                    "Internal CSV must contain transaction_id and amount columns."
                )

            bank_df["transaction_id"] = (
                bank_df["transaction_id"].astype(str).str.strip()
            )

            internal_df["transaction_id"] = (
                internal_df["transaction_id"].astype(str).str.strip()
            )

            bank_df["amount"] = pd.to_numeric(
                bank_df["amount"], errors="raise"
            )

            internal_df["amount"] = pd.to_numeric(
                internal_df["amount"], errors="raise"
            )

            if bank_df["transaction_id"].duplicated().any():
                raise ValueError(
                    "Bank CSV contains duplicate transaction IDs."
                )

            if internal_df["transaction_id"].duplicated().any():
                raise ValueError(
                    "Internal CSV contains duplicate transaction IDs."
                )

            merged = pd.merge(
                bank_df[["transaction_id", "amount"]],
                internal_df[["transaction_id", "amount"]],
                on="transaction_id",
                how="outer",
                suffixes=("_bank", "_internal"),
                indicator=True
            )

            results = []

            for _, row in merged.iterrows():

                if row["_merge"] == "left_only":
                    status = "Bank Only"

                elif row["_merge"] == "right_only":
                    status = "Internal Only"

                elif row["amount_bank"] == row["amount_internal"]:
                    status = "Matched"

                else:
                    status = "Amount Mismatch"

                results.append({
                    "transaction_id": row["transaction_id"],
                    "bank_amount": row["amount_bank"],
                    "internal_amount": row["amount_internal"],
                    "status": status
                })

                ReconciliationRecord.objects.update_or_create(
                    transaction_id=str(row["transaction_id"]),
                    defaults={
                        "bank_amount": (
                            row["amount_bank"]
                            if pd.notna(row["amount_bank"])
                            else None
                        ),
                        "internal_amount": (
                            row["amount_internal"]
                            if pd.notna(row["amount_internal"])
                            else None
                        ),
                        "status": status
                    }
                )

            return render(request, "reconciliation/results.html", {
                "results": results,
                "total": len(results),
                "matched": sum(
                    r["status"] == "Matched" for r in results
                ),
                "mismatched": sum(
                    r["status"] == "Amount Mismatch" for r in results
                ),
                "missing": sum(
                    r["status"] in ["Bank Only", "Internal Only"]
                    for r in results
                ),
            })

        except Exception as error:
            return render(request, "reconciliation/upload.html", {
                "error": str(error)
            })

    return render(request, "reconciliation/upload.html")


def exception_management(request):

    if request.method == "POST":

        record_id = request.POST.get("record_id")
        exception_status = request.POST.get("exception_status")
        notes = request.POST.get("notes")

        record = ReconciliationRecord.objects.get(id=record_id)

        if exception_status in ["Open", "In Progress", "Resolved"]:
            record.exception_status = exception_status

        record.notes = notes
        record.save()

    exceptions = ReconciliationRecord.objects.exclude(
        status="Matched"
    )

    search_query = request.GET.get("search", "")
    selected_status = request.GET.get("status", "")

    if search_query:
        exceptions = exceptions.filter(
            transaction_id__icontains=search_query
        )

    if selected_status:
        exceptions = exceptions.filter(
            exception_status=selected_status
        )

    exceptions = exceptions.order_by("-created_at")

    return render(
        request,
        "reconciliation/exceptions.html",
        {
            "exceptions": exceptions,
            "search_query": search_query,
            "selected_status": selected_status,
        }
    )


def download_report(request):

    records = ReconciliationRecord.objects.all().order_by("transaction_id")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="FinRecon_Report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Transaction ID",
        "Bank Amount",
        "Internal Amount",
        "Reconciliation Status",
        "Exception Status",
        "Notes"
    ])

    for record in records:
        writer.writerow([
            record.transaction_id,
            record.bank_amount if record.bank_amount is not None else "",
            record.internal_amount if record.internal_amount is not None else "",
            record.status,
            record.exception_status,
            record.notes
        ])

    return response
