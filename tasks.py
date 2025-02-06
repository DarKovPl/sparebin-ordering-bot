from configuration.settings import check_dirs_exist
from modules.robot_spare_website import (
    configure_browser_context, 
    open_website,
    manage_popup,
    get_model_info,
    refresh_page,
    fill_the_form,
    check_receipt_appeared,
    extract_receipt_data,
    get_image_of_robot,
    order_another_robot,
)
from modules.files_operations import (
    download_file, 
    get_csv_data,
    store_receipt_as_pdf,
    zip_folders,
    delete_after_zip_folders
)
from robocorp.tasks import task

@task
def order_robots_from_RSB():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    Deletes the folders with the receipts and the images after zipping.
    """
    check_dirs_exist()
    download_file()

    orders = get_csv_data()
    print(f"\nOrders table info: {orders}\n")

    configure_browser_context()
    open_website()
    manage_popup()

    model_info = get_model_info()

    transaction_attempts = 1
    err_message = str()
    for transaction_no, order in enumerate(orders):
        print(f"Robot transaction: {transaction_no + 1} - {order}")

        if transaction_attempts > 2:
            print(err_message)
            raise Exception(err_message)

        for attempt in range(1, 4):
            if attempt > 1:
                print(f"Error while filling the form. Retrying number ({attempt})...")
                refresh_page()
                manage_popup()

            try:
                fill_the_form(order, model_info)
                check_receipt_appeared(order, transaction_no + 1)
                receipt_data = extract_receipt_data()
                image_size, image_path = get_image_of_robot(order, transaction_no + 1)
                order_another_robot()
                manage_popup()
                store_receipt_as_pdf(image_size, image_path, receipt_data, order, transaction_no + 1)

                transaction_attempts = 1
                break
            except Exception as e:
                print(f"Failed to fill the form: {e}.")
        else:
            err_message = f"Failed to fill the form after {transaction_attempts} transaction attempts. Bot is stopping."
            transaction_attempts += 1

    folders_to_delete = zip_folders()
    delete_after_zip_folders(folders_to_delete)
    print("Robot orders completed successfully.")