from agent import run_agent, display_result

def main():
    print("\n🤖 Smart Contract AI Agent\n")
    address = input("Enter contract address: ").strip()

    try:
        state = run_agent(address)
        display_result(state)
    except Exception as e:
        print("❌ Error:", str(e))

if __name__ == "__main__":
    main()
