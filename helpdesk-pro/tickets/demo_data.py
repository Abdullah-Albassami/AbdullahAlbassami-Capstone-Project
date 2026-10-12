"""Fictional fixture identities; no passwords or private information."""

from datetime import datetime, timedelta, timezone

from .constants import Priority, Role, Status

SEED_TIME = datetime(2026, 10, 10, 6, 0, tzinfo=timezone.utc)
USERS = (
    (9001, "employee1", "Nora", "Demo", Role.EMPLOYEE),
    (9002, "employee2", "Omar", "Demo", Role.EMPLOYEE),
    (9003, "technician1", "Lina", "Demo", Role.TECHNICIAN),
    (9004, "technician2", "Sami", "Demo", Role.TECHNICIAN),
    (9005, "itadmin", "Rana", "Demo", Role.IT_ADMIN),
)
DEPARTMENTS = ((1101, "Finance"), (1102, "Human Resources"), (1103, "Operations"), (1104, "Sales"))
CATEGORIES = (
    (1201, "Hardware", "Workstations, printers and physical equipment."),
    (1202, "Software", "Installed applications and business software."),
    (1203, "Network", "Wi-Fi, VPN and network connectivity."),
    (1204, "Accounts", "Access requests and account assistance."),
    (1205, "Unused", "No tickets; demonstrates permitted category deletion."),
)
# ID, title, description, category, department, requester, priority, status, assignee
TICKETS = (
    (10001, "Printer not responding", "The finance printer shows offline and queued invoices do not print.", 1201, 1101, 9001, Priority.HIGH, Status.NEW, None),
    (10002, "Spreadsheet application crashes", "The application closes when opening the monthly staffing worksheet.", 1202, 1102, 9002, Priority.MEDIUM, Status.NEW, None),
    (10003, "Warehouse Wi-Fi unavailable", "The operations laptop cannot connect to the internal Wi-Fi network.", 1203, 1103, 9001, Priority.HIGH, Status.NEW, None),
    (10004, "Laptop overheating", "The sales laptop becomes unusually hot during video meetings.", 1201, 1104, 9002, Priority.MEDIUM, Status.ASSIGNED, 9003),
    (10005, "ERP report layout issue", "Exported invoice reports have incorrect column widths.", 1202, 1101, 9001, Priority.LOW, Status.ASSIGNED, 9003),
    (10006, "New employee account request", "Please prepare access to the training system for a fictional new starter.", 1204, 1102, 9002, Priority.HIGH, Status.ASSIGNED, 9004),
    (10007, "Slow workstation", "The operations workstation takes several minutes to open its inventory application.", 1201, 1103, 9001, Priority.HIGH, Status.IN_PROGRESS, 9003),
    (10008, "VPN connection drops", "The sales VPN disconnects repeatedly while working from the demo remote office.", 1203, 1104, 9002, Priority.MEDIUM, Status.IN_PROGRESS, 9004),
    (10009, "Monitor flickering", "The second finance monitor flickers when connected through the docking station.", 1201, 1101, 9001, Priority.MEDIUM, Status.RESOLVED, 9003),
    (10010, "Training portal access restored", "The fictional training account was unable to sign in.", 1204, 1102, 9002, Priority.MEDIUM, Status.RESOLVED, 9004),
    (10011, "Duplicate software request", "This request duplicates a software installation already arranged by the team.", 1202, 1103, 9001, Priority.LOW, Status.CANCELLED, None),
    (10012, "Office network check withdrawn", "The planned sales meeting moved and this network check is no longer required.", 1203, 1104, 9002, Priority.LOW, Status.CANCELLED, 9004),
)
COMMENTS = (
    (20001, 10001, 9005, "Request received; please leave the printer powered on for inspection."),
    (20002, 10007, 9003, "Checking startup applications and available disk space."),
    (20003, 10008, 9002, "The connection also dropped during this morning's demonstration call."),
    (20004, 10009, 9003, "The faulty display cable has been replaced and the image is stable."),
)
RESOLUTIONS = {
    10009: "Replaced the display cable and verified both monitors remain stable.",
    10010: "Restored the training account access and verified a successful sign-in.",
}


def ticket_created_at(pk):
    return SEED_TIME + timedelta(minutes=pk - 10001)


def comment_created_at(pk):
    return SEED_TIME + timedelta(minutes=15 + pk - 20001)
