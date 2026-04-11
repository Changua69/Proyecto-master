import API from "./api"

export const createReservation = (data: any) => {
  return API.post("/reservations/create", data)
}