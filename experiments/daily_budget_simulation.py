
class DailyBudget:

    def __init__(self, daily_limit):

        self.daily_limit = daily_limit
        self.used_tokens = 0

    def consume(self, tokens):

        if tokens <= 0:
            raise ValueError("Tokens must be positive.")

        if self.used_tokens + tokens > self.daily_limit:
            return False

        self.used_tokens += tokens
        return True

    def remaining(self):

        return self.daily_limit - self.used_tokens


def main():

    print("=" * 50)
    print("THE RELAY - DAILY BUDGET SIMULATION")
    print("=" * 50)

    budget = DailyBudget(daily_limit=1000)

    requests = [
        {"request_id": 1, "tokens": 250},
        {"request_id": 2, "tokens": 300},
        {"request_id": 3, "tokens": 200},
        {"request_id": 4, "tokens": 250},
        {"request_id": 5, "tokens": 100}
    ]

    successful = 0
    rejected = 0

    for request in requests:

        request_id = request["request_id"]
        tokens = request["tokens"]

        print(f"\nRequest {request_id}")
        print("Requested Tokens:", tokens)

        result = budget.consume(tokens)

        if result:

            successful += 1

            print("Status: SUCCESS")
            print("Remaining Budget:", budget.remaining())

        else:

            rejected += 1

            print("Status: REJECTED")
            print("Reason: Daily token budget exhausted.")
            print("Remaining Budget:", budget.remaining())

    print("\n" + "=" * 50)
    print("FINAL SUMMARY")
    print("=" * 50)

    print("Daily Budget:", budget.daily_limit)
    print("Tokens Used:", budget.used_tokens)
    print("Remaining Tokens:", budget.remaining())
    print("Successful Requests:", successful)
    print("Rejected Requests:", rejected)


if __name__ == "__main__":
    main()
