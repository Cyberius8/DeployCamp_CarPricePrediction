import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';

const duration_200 = new Trend('duration_200', true);
const duration_429 = new Trend('duration_429', true);

export const options = {
  scenarios: {
    load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5s', target: 400 },
        { duration: '10s', target: 400 },
        { duration: '5s', target: 0 },
      ],
    },
  },
};


export default function () {

  // for frontend testing
  // const url = 'https://predictcarprice.my.id/';
  // const res = http.get(url);

  // for backend testing
  const url = 'https://predictcarprice.my.id/predict';
  const payload = JSON.stringify({
    fuelsystem: 'mpfi',
    brand: 'volvo',
    wheelbase: 0,
    carlength: 0,
    carwidth: 0,
    curbweight: 0,
    enginesize: 0,
    boreratio: 0,
    horsepower: 0,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);
  
  if (res.status === 200) {
    duration_200.add(res.timings.duration);
  }
  if (res.status === 429) {
    duration_429.add(res.timings.duration);
  }
  sleep(1);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'status is 429 (rate limited)': (r) => r.status === 429,
  });
}
