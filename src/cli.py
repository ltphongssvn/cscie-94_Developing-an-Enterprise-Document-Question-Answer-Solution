# src/cli.py
# Full path: /src/cli.py
import argparse
from src.document_qa import DocumentQASystem


def interactive_mode(qa_system):
    """Run interactive Q&A session."""
    print("\n" + "=" * 80)
    print("Interactive Q&A Mode - Type 'exit' or 'quit' to end")
    print("=" * 80 + "\n")

    while True:
        try:
            question = input("\nYour question: ").strip()

            if question.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if not question:
                continue

            result = qa_system.query(question)
            print(f"\nAnswer: {result['result']}")

            # Show sources if available
            if result.get("source_documents"):
                print(f"\n[Based on {len(result['source_documents'])} sources]")

        except EOFError:
            # Handle piped input or closed stdin
            print("\nEnd of input detected. Exiting...")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Azure OpenAI Document Q&A System")
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory containing documents (default: data)",
    )
    parser.add_argument(
        "--query",
        help="Single query to execute (optional)",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode",
    )

    args = parser.parse_args()

    # Initialize and setup
    qa_system = DocumentQASystem()
    qa_system.setup(data_dir=args.data_dir)

    # Execute query or interactive mode
    if args.query:
        result = qa_system.query(args.query)
        print(f"\nQuestion: {args.query}")
        print(f"Answer: {result['result']}")
    elif args.interactive:
        interactive_mode(qa_system)
    else:
        print("\nSystem ready. Use --query or --interactive flag.")
        print("Example: python src/cli.py --interactive")


if __name__ == "__main__":
    main()
