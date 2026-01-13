export function standardDeviation(array) {
  const n = array.length;
  const mean = array.reduce((a, b) => a + b) / n;
  return Number(Math.sqrt(array.map((x) => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n));
}
