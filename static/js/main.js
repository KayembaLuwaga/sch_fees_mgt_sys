// static/js/main.js file
const tbody = $('#fee-table tbody');

function insert_fee(_this) {
    // Fetch the parent row where the Add button is located
    let parentRow = $(_this).closest('div'); // Adjust this selector based on your actual HTML structure

    // Select input fields for fee description and amount
    let desc = parentRow.find('input[name="fee_desc"]').val();
    let amount = parentRow.find('input[name="amount"]').val();

    // Check if these inputs are empty
    if (desc === "") {
        alert("Please enter a description");
        return;
    }
    if (amount === "" || isNaN(amount) || parseFloat(amount) <= 0) {
        alert("Please enter a valid amount");
        return;
    }

    // Check for duplicate fee descriptions
    let descs = tbody.find('td#desc').map(function() {
        return $(this).text().trim();
    }).get();

    if (descs.includes(desc)) {
        alert("Duplicate fee description");
        return;
    }

    // Append the fee detail to the table
    let elem = `
        <tr>
            <input type="hidden" name="fee_desc[]" value="${desc}">
            <input type="hidden" name="amount[]" value="${amount}">
            <td id="desc">
                <button type="button" class="d-none d-sm-inline-block btn btn-sm btn-danger mr-2"
                onclick="remove_fee($(this))">
                    <i class="fas fa-trash fa-sm text-white-50"></i>
                </button>
                ${desc}
            </td>
            <td id="amount">${amount}</td>
        </tr>
    `;
    tbody.append(elem);

    // Recalculate the total amount
    calculate_total();

    // Clear input fields after adding the fee
    parentRow.find('input[name="fee_desc"]').val('');
    parentRow.find('input[name="amount"]').val('');
}

function remove_fee(_this) {
    $(_this).parent().parent().remove();
    calculate_total();
    let desc = $(_this).parent().parent().find('td#desc').text().trim();
    let amount = $(_this).parent().parent().find('td#amount').text().trim();

    console.log(desc);

    $('#id_fee_desc').val(desc);
    $('#id_amount').val(amount);
}

function calculate_total() {
    let total = 0;
    tbody.find('tr').each(function() {
        total += parseFloat($(this).find('td#amount').text());
    });
    $('#id_total_amount').val(total);
    $('#fee-table tfoot tr td:nth-child(2)').text("$"+total);
}

function get_total_amount(url, cid){
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'course_id': cid,
        }
    }).done(function(data) {
        $('#id_total_fee').val(data.data);
    }
    ).fail(function(data) {
        console.log(data);
    });
}

function get_outstanding_balance(url, eid){
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'enroll_id': eid,
        }
    }).done(function(data) {
        $('#id_balance').val(data.data);
    }
    ).fail(function(data) {
        console.log(data);
    });
}

function printInvoice() {
    let divContents = document.getElementById("invoice").innerHTML;
    let a = window.open('', '', `height=${screen.availHeight}, width=${screen.availWidth}`);
    a.document.write(divContents);
    a.document.close();
    a.print();
}

function validateAndSubmitForm() {
    const feeRows = $('#fee-table tbody tr').length;
    if (feeRows === 0) {
        alert("Please add at least one fee before submitting.");
    } else {
        document.getElementById('student-form').submit();
    }
}

function updateTotalFee(courseSelectElement) {
    var courseId = $(courseSelectElement).val();
    if (courseId) {
        $.ajax({
            url: '/course/get_total_amount/',  // Your endpoint to get the total_amount for a course
            type: 'GET',
            data: {'course_id': courseId},
            success: function(data) {
                $('#id_total_fee').val(data.total_amount);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching total amount: ", status, error);
            }
        });
    } else {
        $('#id_total_fee').val('');  // Clear if no course is selected
    }
}

// Document ready function to attach event handlers and initialize
$(document).ready(function() {
    // Attach the event handler to the course_id field
    $('#id_course_id').change(function() {
        updateTotalFee(this);
    });

    // Update student_id based on selected student_number
    $('#id_student_number').change(function() {
        var studentId = $(this).val();
        $('#id_student_id').val(studentId);
    });
});

$(document).ready(function() {
    // Function to update the total_fee based on selected course_id
    window.updateTotalFee = function(courseSelectElement) {
        var courseId = $(courseSelectElement).val();
        if (courseId) {
            $.ajax({
                url: '/course/get_total_amount/',  // Your endpoint to get the total_amount for a course
                type: 'GET',
                data: {'course_id': courseId},
                success: function(data) {
                    $('#id_total_fee').val(data.total_amount);
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching total amount: ", status, error);
                }
            });
        } else {
            $('#id_total_fee').val('');  // Clear if no course is selected
        }
    };

    // Update student_id based on selected student_number
    $('#id_student_number').change(function() {
        var studentId = $(this).val();
        $('#id_student_id').val(studentId);
    });

    // Attach the event handler to the course_id field
    $('#id_course_id').change(function() {
        updateTotalFee(this);
    });
});
