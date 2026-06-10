<template>

    <div>

        <h2>Booking History</h2>

        <div v-for="booking in bookingList" :key="booking.booking_id">

            <p>
                User:
                {{ booking.user_name }}
            </p>

            <p>
                Email:
                {{ booking.user_email }}
            </p>

            <p>
                Trek:
                {{ booking.trek_name }}
            </p>

            <p>
                Status:
                {{ booking.status }}
            </p>

            <p>
                Payment:
                {{ booking.payment_status }}
            </p>

            <p>
                Date:
                {{ booking.booking_date }}
            </p>

            <hr>

        </div>

    </div>

</template>

<script>
import axios from "axios"

export default {

    name: "BookingHistory",

    data() {
        return {
            bookingList: []
        }
    },

    async mounted() {

        try {

            const token =
                localStorage.getItem("token")

            const response =
                await axios.get(
                    "http://localhost:5000/api/admin/bookings",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            this.bookingList = response.data

        }

        catch(error) {

            console.error(error)

        }

    }

}
</script>