from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
from .models import BusOrganisation, Route, Bus, Schedule, Ticket
from .forms import TicketForm
from .utils import render_to_pdf
import uuid
import phonenumbers
import logging
import africastalking
import re
# Create your views here.
logger = logging.getLogger(__name__)


def index(request):
    '''
    landing page
    '''
    return render(request, 'index.html')


def search_results(request):
    '''
    View function to get the the requested departure and arrival locations from the database and display to the user
    '''
    try:
        title = 'Result'

        if ('depature-location' in request.GET and request.GET['depature-location']) and ('arrival-location' in request.GET and request.GET['arrival-location']) and ('travel-date' in request.GET and request.GET['travel-date']):

            # Get the input departure
            search_departure_location = request.GET.get(
                'depature-location').title()

            # Get the input arrival location
            search_arrival_location = request.GET.get(
                'arrival-location').title()

            # Get the input date
            travel_date = request.GET.get('travel-date')

            # Convert string input to date type
            convert_to_date = datetime.strptime(travel_date, '%Y-%m-%d').date()

            # Get the route
            result_route = Route.get_search_route(
                search_departure_location, search_arrival_location)
            print(result_route)

            # Check if route exists found
            if result_route != None:

                # Schedule with the same depature date
                schedule_with_depature_date = Schedule.get_departure_buses(
                    convert_to_date, result_route.id)

                if len(schedule_with_depature_date) > 0:

                    for schedule in schedule_with_depature_date:

                        estimation_duration = Schedule.get_travel_estimation(
                            schedule.id)

                    return render(request, 'search.html', {'title': title, 'search_departure_location': search_departure_location, 'search_arrival_location': search_arrival_location, 'convert_to_date': convert_to_date, 'buses': schedule_with_depature_date, 'estimation_duration': estimation_duration})

                else:
                    print('no scheduled buses')
                    no_scheduled_bus_message = 'No scheduled buses'

                    return render(request, 'search.html', {'title': title, 'no_scheduled_bus_message': no_scheduled_bus_message, 'search_departure_location': search_departure_location, 'search_arrival_location': search_arrival_location, 'convert_to_date': convert_to_date})

            # Otherwise
            else:

                no_route_message = 'No Buses on that Route, More Routes Comming Soon!'

                return render(request, 'search.html', {'title': title, 'no_route_message': no_route_message, 'search_departure_location': search_departure_location, 'search_arrival_location': search_arrival_location, 'convert_to_date': convert_to_date})

    except ObjectDoesNotExist:

        return redirect(Http404)


def bus_details(request, bus_schedule_id):
    '''
    View function to display a form for the user to fill to get a ticket
    '''
    try:
        # args = {}

        selected_bus = Schedule.get_single_schedule(bus_schedule_id)

        title = f'{selected_bus.bus.bus_organisation} Schedule Details'

        estimation_duration = Schedule.get_travel_estimation(bus_schedule_id)

        if request.method == 'POST':

            form = TicketForm(request.POST)

            if form.is_valid():

                ticket = form.save(commit=False)

                ticket.schedule = selected_bus

                ticket.ticket_number = uuid.uuid4()

                ticket.save()

                ticket_id = ticket.id

                return redirect(mobile_payment, ticket_id)

        else:

            form = TicketForm()

        # args['form'] = form

        return render(request, 'bus_details.html', {'title': title, 'form': form, 'selected_bus': selected_bus, 'estimation_duration': estimation_duration})

    except ObjectDoesNotExist:

        return redirect(Http404)


def mobile_payment(request, ticket_id):
    '''
    Function that carries out the payment process
    '''
    # Get ticket with a given id
    ticket = Ticket.get_single_ticket(ticket_id)

    # Get the route and convert to string
    bus_route = str((ticket.schedule.bus.bus_organisation.name))
    # print(type(bus_route))

    # Get the phone number
    phone_number = ticket.phone_number
    # print(type(phone_number))

    # Get the ticket price and convert Decimal to int
    ticket_price = float(ticket.schedule.price)
    # print(type(ticket_price))

    # init payments
    username = "sandbox"
    apiKey = "a5f09988fe43adee963c0df9d4962738bbd1807b35a7bdf95e3b1dd3c14926f8"

    africastalking.initialize(username, apiKey)
    payment = africastalking.Payment

    # Specify the name of your Africa's Talking payment product
    productName = "BusAcme"

    # The phone number of the customer checking out
    phoneNumber = "+254" + phone_number.lstrip("0")  # phone_number
    
    # logger.info("Phone: %s" % str(phone_number))

    # The 3-Letter ISO currency code for the checkout amount
    currencyCode = "KES"

    # The checkout amount
    amount = ticket_price
    # print(amount)

    # Any metadata that you would like to send along with this request
    # This metadata will be  included when we send back the final payment notification
    metadata = {"product": "525900",
                "productCode": "5449"}

    # Initiate the checkout. If successful, you will get back a transactionId
    transaction_id = payment.mobile_checkout(productName, phoneNumber,
                                                 currencyCode,
                                                 amount,
                                                 metadata)


    ticket.transaction_code = transaction_id
    ticket.save()


    return redirect('/ticket/' + str(ticket_id))




def generate_view(request, ticket_id):

    gotten_ticket = Ticket.get_single_ticket(ticket_id)

    pdf = render_to_pdf('pdf/ticket.html', {'gotten_ticket': gotten_ticket})

    if pdf:

        response = HttpResponse(pdf, content_type='application/pdf')

        filename = "Ticket_%s.pdf" % (gotten_ticket.ticket_number)

        content = "inline; filename='%s'" % (filename)

        download = request.GET.get("download")

        if download:

            content = "attachment; filename='%s'" % (filename)

        response['Content-Disposition'] = content

        return response

    return HttpResponse('Not Found')
